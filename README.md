# SolidWorks Migration Suite for FreeCAD

This is a comprehensive suite of themes and scripts designed to make the transition from SolidWorks to FreeCAD smoother. It adjusts FreeCAD's appearance, terminology, and tool layout to be more familiar to SolidWorks users.

This addon was generated with the assistance of the Gemini CLI.

***

## Features

*   **Dual Themes:** Includes both a "SolidWorks Light" and "SolidWorks Dark" theme that can be selected in FreeCAD's preferences.
*   **Terminology Mapping:** Automatically renames common FreeCAD commands to their SolidWorks equivalents (e.g., `PartDesign_Pad` becomes "Extruded Boss/Base").
*   **SolidWorks-style Toolbars:** Programmatically creates new toolbars (`SW_Sketch`, `SW_Features`, etc.) that group commands in a layout familiar to SolidWorks users.
*   **"S-Key" Context Palette:** An optional macro that provides a mouse-centered palette of tools relevant to your current workbench (Part Design or Sketcher).
*   **Smart Line Tool:** An optional macro that mimics the SolidWorks behavior of switching from the Line tool to the Arc tool by pressing the 'A' key.

## Installation

This addon is designed to be installed via the FreeCAD Addon Manager using a custom Git repository.

1.  **Start FreeCAD.**
2.  Navigate to **Tools > Addon Manager**.
3.  In the Addon Manager, click the **"..."** button at the top right to open "Addon manager options".
4.  Under the **"Custom repositories"** tab, click the **"Add..."** button.
5.  Enter the URL of your GitHub repository (e.g., `https://github.com/YourUsername/YourRepoName`).
6.  Click **OK** to close the options.
7.  The Addon Manager may prompt you to refresh. Once refreshed, search for "SolidWorks Migration Suite".
8.  Select the addon and click **Install**.
9.  Restart FreeCAD as prompted.

## Usage

### Themes, Naming, and Toolbars
Upon restarting FreeCAD after installation, the core features will be automatically activated:

*   **Themes:** Go to **Edit > Preferences > General**. In the "Style sheet" dropdown, you will now find `SolidWorks_Light` and `SolidWorks_Dark`.
*   **Toolbars & Naming:** The `sw_loader.py` script runs automatically on startup. It will rename the commands and create the new `SW_...` toolbars.

### Optional Macros
The S-Key and Smart Line tools are macros that you must assign to a shortcut or custom toolbar button manually.

1.  Go to **Tools > Customize...**.
2.  Go to the **Macros** tab.
3.  Find `s_key_palette.py` and `smart_line.py` in the list. You can add them to a custom toolbar here.
4.  To assign a keyboard shortcut (recommended for the S-Key), go to the **Keyboard** tab.
    *   Find the macro by its name (e.g., "s_key_palette").
    *   Select it, and assign a new shortcut (e.g., the `S` key).
    *   Click **Assign**.
