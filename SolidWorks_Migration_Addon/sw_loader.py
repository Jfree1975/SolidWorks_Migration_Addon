# sw_loader.py
import FreeCADGui as Gui
import FreeCAD
import json
import os

def get_addon_dir():
    """Returns the path to this addon's directory."""
    return os.path.dirname(__file__)

def load_naming_map():
    map_path = os.path.join(get_addon_dir(), "naming_map.json")
    try:
        with open(map_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        FreeCAD.Console.PrintError(f"SW_Loader: Could not load naming_map.json: {e}\n")
        return None

def create_reverse_lookup(naming_map):
    reverse_map = {}
    for workbench, commands in naming_map.items():
        if workbench == "ToolbarGroups": continue
        for fc_cmd, sw_name in commands.items():
            if sw_name not in reverse_map: reverse_map[sw_name] = []
            reverse_map[sw_name].append(fc_cmd)
    return reverse_map

def apply_renaming(naming_map):
    for workbench, commands in naming_map.items():
        if workbench == "ToolbarGroups": continue
        for fc_cmd, sw_name in commands.items():
            try:
                command = Gui.Command.get(fc_cmd)
                if command:
                    command.MenuText = sw_name
                    command.ToolTip = f"{sw_name} ({fc_cmd})"
            except Exception:
                pass

def create_toolbars(naming_map, reverse_lookup_map):
    mw = Gui.getMainWindow()
    toolbar_groups = naming_map.get("ToolbarGroups", {})
    for group_name, sw_command_list in toolbar_groups.items():
        toolbar_name = f"SW_{group_name}"
        existing_toolbar = mw.findChild(Gui.ToolBar, toolbar_name)
        if existing_toolbar:
            mw.removeToolBar(existing_toolbar)
        toolbar = Gui.ToolBar(toolbar_name)
        for sw_name in sw_command_list:
            fc_commands = reverse_lookup_map.get(sw_name)
            if fc_commands:
                toolbar.addCommand(fc_commands[0])
        mw.addToolBar(Gui.TopToolBarArea, toolbar)

def run_migration():
    FreeCAD.Console.PrintMessage("--- Loading SolidWorks Migration Suite ---
")
    naming_map = load_naming_map()
    if not naming_map: return
    reverse_map = create_reverse_lookup(naming_map)
    apply_renaming(naming_map)
    create_toolbars(naming_map, reverse_map)
    FreeCAD.Console.PrintMessage("--- SolidWorks Migration Suite Loaded ---
")

# This code runs when the addon is loaded via the Addon Manager
run_migration()
