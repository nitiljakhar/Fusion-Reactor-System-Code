Fusion Reactor System GUI
This Python program provides a graphical user interface (GUI) to manage a fusion reactor system code. It allows users to select various parameters for different subsystems (like Figures of Merit, Constraints, Build variables, etc.) through an interactive menu and checkboxes. The GUI is built using the Tkinter library.

Features
Modular Parameter Selection:

Supports selection for Figures of Merit, Constraints, Build Variables, and more.
Enables 1D and 2D scans for input data.
Search and Replace:

Find specific text and replace it with new values within the main text editor.
Scrollable Checkbox Menus:

Parameter selection is available via checkboxes for various modules, allowing easy toggling of options.
Dynamic Update:

Updates the state of checkboxes dynamically based on changes in the text box content.
Shortcut Support:

Keyboard shortcuts are included for search (Ctrl+F) and replace (Ctrl+H).
Summary and Execute:

Two main buttons are available to summarize selected options and execute the final command.
Installation
Prerequisites:

Python 3.x
Tkinter library (typically pre-installed with Python)
Clone the Repository:

bash
Copy code
git clone https://github.com/yourusername/fusion-reactor-gui.git
cd fusion-reactor-gui
Run the Program:

bash
Copy code
python3 fusion_gui.py
Usage Instructions
Main Menu
Once the GUI starts, you'll see a menu bar at the top of the window. Here's what each menu option provides:

File:

Open: Opens an existing input file.
Save: Saves the current configuration.
Save As: Saves the current configuration under a new file name.
Search and Replace: Opens a window to search for specific text and optionally replace it in the main text box.
Exit: Closes the application.
Figure-of-Merit:

Opens a checkbox window to select the desired Figures-of-Merit (FoM).
Constraint:

Opens a window to select constraint values.
Iteration:

Opens a window to choose iteration options.
Scan Module
This menu handles sweeping parameters for 1D and 2D scans:

1D:
Select a parameter to sweep and enter the values as a comma-separated list.
2D:
Choose two parameters to sweep in 2D and enter the values for both as comma-separated lists.
Variable Selection (Various Modules)
The menu also offers various categories to select from:

Build:

Opens a menu to select variables related to the build process.
Constraint Variables:

Choose constraints for the fusion reactor setup.
Cost Variables:

Manage cost-related parameters.
Current Drive:

Select options for the current drive system.
Divertor Variables:

Configure the divertor subsystem settings.
Fwbs Variables:

Handle first wall and blanket structure values.
Heat Transport:

Control heat transport-related settings.
Impurity Radiation:

Set parameters for impurity radiation in the plasma.
Numerics:

Fine-tune numerical parameters for the calculations.
CS/pfcoil Variables:

Choose settings for the Central Solenoid (CS) and poloidal field (PF) coils.
Physics Variables:

Adjust key physics variables affecting the fusion reactor.
Pulse Variables:

Manage pulse-related values.
Tfcoil Variables:

Set parameters for the toroidal field (TF) coil.
Text Box and Scrollbar
The main area is a text box where:

The results of your selections will appear.
You can manually enter or modify text.
A vertical scrollbar allows you to navigate the content easily.
Footer Buttons
Summary: This button provides a summary of the current selections and displays them in the text area.
Execute: Executes the selected configuration.
Detailed Features
Checkbox Windows
Each window, such as for Figures-of-Merit or Constraints, provides a list of checkboxes. You can select or deselect parameters, and the state will be retained when reopening the windows.
Dynamic Updates
The application automatically keeps track of selected options and updates them based on the current state of the main text box. This prevents inconsistencies between what is displayed and what is selected.
Search and Replace
The program offers a search and replace feature to quickly modify parameters within the main text area:

Find: Highlights all instances of the searched word.
Replace: Replaces all occurrences of the searched word with the new word.
Customization
To add more Figures of Merit, Constraints, or other parameters, update the respective dictionaries in the code. For example, to add a new constraint, modify the constraint_values dictionary inside Constraint_checkboxes().
Shortcuts
Ctrl + F: Opens the search window to find text in the main text box.
Ctrl + H: Opens the replace window to find and replace text.
Contributing
Feel free to fork the repository, make modifications, and send a pull request. Contributions are welcome!

License
This project is licensed under the MIT License.

Example Screenshot
If you'd like to provide visuals, you can include example screenshots of the application to make it easier for users to understand the interface.

This README.md provides users with all the information needed to understand, install, and use your fusion reactor system GUI. You can customize it further based on your project’s specific requirements.
