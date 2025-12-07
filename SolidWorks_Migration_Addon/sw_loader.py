# sw_loader.py
import FreeCADGui as Gui
import FreeCAD
import json
import os
import shutil

def install_themes():
    """
    Copies the theme .qss files from the addon directory to the user's
    FreeCAD Gui/Stylesheets directory, where they can be found by the
    Preferences dialog.
    """
    try:
        addon_dir = os.path.dirname(__file__)
        stylesheet_dir = os.path.join(FreeCAD.getUserAppDataDir(), "Gui", "Stylesheets")

        if not os.path.exists(stylesheet_dir):
            os.makedirs(stylesheet_dir)
            FreeCAD.Console.PrintMessage("SW_Loader: Created user Stylesheets directory.\n")

        themes = ["SolidWorks_Light.qss", "SolidWorks_Dark.qss"]
        for theme_file in themes:
            source_path = os.path.join(addon_dir, theme_file)
            dest_path = os.path.join(stylesheet_dir, theme_file)
            # Copy the file if it doesn't exist or if the source is newer
            if not os.path.exists(dest_path) or os.path.getmtime(source_path) > os.path.getmtime(dest_path):
                shutil.copyfile(source_path, dest_path)
                FreeCAD.Console.PrintMessage(f"SW_Loader: Installed/Updated theme '{theme_file}'.\n")
    except Exception as e:
        FreeCAD.Console.PrintError(f"SW_Loader: Could not install themes automatically: {e}\n")

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
    # This now runs first to ensure themes are in place
    install_themes()
    
    FreeCAD.Console.PrintMessage("--- Loading SolidWorks Migration Suite ---\n")
    naming_map = load_naming_map()
    if not naming_map: return
    reverse_map = create_reverse_lookup(naming_map)
    apply_renaming(naming_map)
    create_toolbars(naming_map, reverse_map)
    FreeCAD.Console.PrintMessage("--- SolidWorks Migration Suite Loaded ---\n")

# This code runs when the addon is loaded by FreeCAD
run_migration()
