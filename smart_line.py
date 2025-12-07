# smart_line.py
import FreeCADGui as Gui
from PySide import QtCore

class SmartLineTool:
    def __init__(self):
        self.view = Gui.activeDocument().activeView()
        self.observer = KeyPressObserver()
        self.view.addEventCallback("SoKeyboardEvent", self.observer.handle_event)
        self.observer.key_pressed.connect(self.handle_key_press)
        Gui.runCommand('Sketcher_CreateLine')

    def handle_key_press(self, key):
        if key == 'A':
            Gui.runCommand('Sketcher_CreateArc')
            self.stop()

    def stop(self):
        self.view.removeEventCallback("SoKeyboardEvent", self.observer.handle_event)

class KeyPressObserver(QtCore.QObject):
    key_pressed = QtCore.Signal(str)
    def handle_event(self, event_callback):
        if event_callback["Event"].isOfType(Gui.SoKeyboardEvent.getClassTypeId()):
            if event_callback["Event"].getState() == Gui.SoKeyboardEvent.DOWN:
                self.key_pressed.emit(event_callback["Event"].getKey().name)
        return False

def run_smart_line():
    if not Gui.activeWorkbench().__class__.__name__ == 'SketcherWorkbench' or not Gui.ActiveDocument.ActiveView.getEditingSketch():
        FreeCAD.Console.PrintWarning("Smart Line: Please enter a sketch editing mode first.\n")
        return
    global smart_line_tool
    smart_line_tool = SmartLineTool()
