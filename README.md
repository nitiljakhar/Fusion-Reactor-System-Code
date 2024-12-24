<h1>Fusion Reactor System Code</h1>
<h3> GUI</h3> 

This Python program provides a graphical user interface (GUI) to manage a fusion reactor system code PROCESS ([https://github.com/ukaea/PROCESS](https://github.com/ukaea/PROCESS)). The GUI simplifies the management of fusion reactor parameters, making the process faster and more accessible.

PROCESS is the reactor systems code at the ([UK Atomic Energy Authority](https://ccfe.ukaea.uk/)). Here are the ([PROCESS docs](https://ukaea.github.io/PROCESS/)) and ([Webpage](https://ccfe.ukaea.uk/resources/process/)).

![image alt](https://github.com/nitiljakhar/Fusion-Reactor-System-Code/blob/99246873ad3465b10078f8322d0e1c660e64968b/Images/Screenshot%202024-12-24%20153300.png)
## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage Instructions](#usage-instructions)
5. [Main Menu Options](#main-menu-options)
6. [Footer Buttons](#footer-buttons)
7. [Detailed Features](#detailed-features)
8. [Customization](#customization)
9. [Shortcuts](#shortcuts)
10. [Contributing](#contributing)
11. [License](#license)
12. [Founder](#founder)

---

## Overview
The Fusion Reactor System GUI provides an interactive interface to manage and configure parameters for the fusion reactor system. It includes modular options for Figures of Merit, Constraints, Build variables, and other essential modules. The GUI is designed for ease of use, featuring menus, checkboxes, and a scrollable text box for displaying configurations and results.

## Features
- **Modular Parameter Selection**: Easily select Figures of Merit, Constraints, Build Variables, and more.
- **1D and 2D Parameter Scans**: Configure sweeps for input data.
- **Search and Replace**: Quickly locate and modify text within the main text editor.
- **Dynamic Updates**: Checkbox states dynamically update based on the content of the text box.
- **Shortcut Support**: Includes keyboard shortcuts for common actions (e.g., Ctrl+F for search).
- **Execute and Summary Commands**: Execute the process and view a summary of results.

## Installation

### Prerequisites
- Python 3
- Tkinter library (typically pre-installed with Python)

### Steps to Install
1. Clone the repository:
   ```bash
   git clone https://github.com/nitiljakhar/Fusion-Reactor-System-Code.git
   cd Fusion-Reactor-System-Code
2. Run the program:
   ```bash
   python3 System_code.py

## Usage Instructions
### Main Interface
When the program starts, the GUI displays a main menu bar, a toolbar with buttons for various parameters, a scrollable text box, and footer buttons for "Execute" and "Summary".


## Main Menu Options
### File Menu
- **Open**: Load an existing input file.
- **Save**: Save the current configuration.
- **Save As**: Save the configuration under a new file name.
- **Search and Replace**: Open a tool to search and replace text.
- **Exit**: Close the application.
### Edit Menu
- Includes options for modifying text or settings in the GUI.
### View Menu
- Toggle between modes such as Night Mode.
### Variables Menu
- Provides access to parameter selection modules such as Figures of Merit, Constraints, Iteration, Build Variables, and more.
## Footer Buttons
- **Execute**: Executes the DAT file using WSL command: f'process -i "{file_name}"'.
- **Summary**: Displays the summary of results using WSL command: f'./plot_proc.py -f "{file_name}_MFILE.DAT"'.
## Detailed Features
### Parameter Selection
- **Figures of Merit**: Select desired metrics for analysis.
- **Constraints**: Define limits and constraints for the reactor setup.
- **Build Variables**: Configure parameters related to the build process.
Numerics, Heat Transport, and More: Fine-tune advanced parameters.
### Scrollable Checkbox Menus
- Navigate through a variety of options using scrollable checkboxes.
### Search and Replace
- **Find**: Highlights all matches for the search term.
- **Replace**: Replaces all instances of a search term with the new input.
## Customization
- To add or modify parameters, update the respective dictionaries in the source code. For example, to add a new constraint, edit the constraint_values dictionary in the Constraint_checkboxes() function.

## Shortcuts
- **Ctrl + C: Copy selected items.
- **Ctrl + X: Cut selected items.
- **Ctrl + V: Paste copied or cut items.
- **Ctrl + Z: Undo the previous action.
- **Ctrl + Y: Redo the previous action.
- **Ctrl + F: Open the search window to find text or items.
- **Ctrl + H: Open the replace window to find and replace text.
- **Ctrl + S: Save the current file or document.
- **Ctrl + Shift + S: Save as the current file or document.
- **Ctrl + O: Open an existing file or document.
- **Ctrl + Q: Quit or exit the application.
- **Ctrl + "+": Zoom in the text.
- **Ctrl + "-": Zoom out the text.


  
## Contributing
Contributions are welcome! To contribute:
- Fork the repository.
- Make modifications.
- Submit a pull request.


## Founder
### Nitil Jakhar
- **Email:** [nitiljakhar1904jacs@gmail.com](mailto:nitiljakhar1904jacs@gmail)
- **Degree:** Computer Science Engineer
- **University:** Chandigarh University, Mohali, India
