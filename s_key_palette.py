# s_key_palette.py
import FreeCADGui as Gui
import FreeCAD
import json
import os
from PySide import QtCore, QtGui

class S_KeyPalette(QtGui.QDialog):
    def __init__(self, parent=None):
        super(S_KeyPalette, self).__init__(parent, QtCore.Qt.Popup)
        self.addon_dir = os.path.dirname(__file__)
        self.naming_map = self.load_naming_map()
        self.reverse_lookup_map = self.create_reverse_lookup(self.naming_map)
        self.initUI()
        self.populate_tools()
        self.move_to_cursor()

    def initUI(self):
        self.setStyleSheet("QDialog { background-color: rgba(50,50,50,0.9); border: 1px solid #555; border-radius: 5px; } QToolButton { background-color: #404040; color: #E0E0E0; border: 1px solid #606060; padding: 8px; min-width: 80px; min-height: 50px; } QToolButton:hover { background-color: #5A6A7A; border: 1px solid #0078D7; }")
        self.grid_layout = QtGui.QGridLayout(self)
        self.grid_layout.setSpacing(5)
        self.setLayout(self.grid_layout)

    def load_naming_map(self):
        map_path = os.path.join(self.addon_dir, "naming_map.json")
        try:
            with open(map_path, 'r') as f: return json.load(f)
        except Exception: return {}

    def create_reverse_lookup(self, naming_map):
        if not naming_map: return {}
        reverse_map = {}
        for wb, cmds in naming_map.items():
            if wb == "ToolbarGroups": continue
            for fc, sw in cmds.items():
                if sw not in reverse_map: reverse_map[sw] = fc
        return reverse_map

    def populate_tools(self):
        commands = self.get_contextual_commands()
        if not commands: self.close(); return
        cols = 3
        for i, sw_name in enumerate(commands):
            fc_cmd_id = self.reverse_lookup_map.get(sw_name)
            if fc_cmd_id and Gui.Command.get(fc_cmd_id):
                self.add_tool_button(fc_cmd_id, sw_name, i // cols, i % cols)

    def get_contextual_commands(self):
        if not self.naming_map: return []
        groups = self.naming_map.get("ToolbarGroups", {})
        wb_name = Gui.activeWorkbench().__class__.__name__
        if wb_name == "SketcherWorkbench": return groups.get("Sketch", [])
        elif wb_name == "PartDesignWorkbench": return groups.get("Features", [])
        elif wb_name == "TechDrawWorkbench": return groups.get("Drawing", [])
        else: return []

    def add_tool_button(self, command_id, text, row, col):
        button = QtGui.QToolButton()
        cmd = Gui.Command.get(command_id)
        button.setText(text); button.setIcon(cmd.getIcon()); button.setIconSize(QtCore.QSize(32, 32)); button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        button.clicked.connect(lambda: self.execute_command(command_id))
        self.grid_layout.addWidget(button, row, col)

    def execute_command(self, command_id):
        self.close(); Gui.runCommand(command_id)

    def move_to_cursor(self):
        self.move(QtGui.QCursor.pos().x() - self.width()/2, QtGui.QCursor.pos().y() - self.height()/2)

    def leaveEvent(self, event): self.close()

dialog = None
def show_palette():
    global dialog
    main_window = Gui.getMainWindow()
    dialog = S_KeyPalette(main_window)
    dialog.show()
