<h1>Fusion Reactor System Code</h1>
<h3>GUI</h3> 
This Python program provides a graphical user interface (GUI) to manage a fusion reactor system code. It allows users to select various parameters for different subsystems (like Figures of Merit, Constraints, Build variables, etc.) through an interactive menu and checkboxes. The GUI is built using the Tkinter library.

 <h2>Features</h2>
 <ul>
      <li><b>Modular Parameter Selection:</b>
            <ul>
                <li>Supports selection for Figures of Merit, Constraints, Build Variables, and more.</li>
                <li>Enables 1D and 2D scans for input data.
</li>
            </ul>
      </li>
      <li><b>Search and Replace:</b>
            <ul>
                <li>Find specific text and replace it with new values within the main text editor.</li>
            </ul>
      </li>
      <li><b>Scrollable Checkbox Menus:</b>
            <ul>
                <li>Parameter selection is available via checkboxes for various modules, allowing easy toggling of options.</li>
            </ul>
      </li>
      <li><b>Dynamic Update:</b>
            <ul>
                <li>Updates the state of checkboxes dynamically based on changes in the text box content.</li>
            </ul>
      </li>
      <li><b>Shortcut Support:</b>
            <ul>
                <li>Keyboard shortcuts are included for search <code>(Ctrl+F)</code> and replace <code>(Ctrl+H)</code>.</li>
            </ul>
      </li>
      <li><b>Summary and Execute:</b>
            <ul>
                <li>Two main buttons are available to summarize selected options and execute the final command.</li>
            </ul>
      </li>  
</ul>

<h2>Installation</h2>
 <ul>
      <li><b>Prerequisites:</b>
            <ul>
                <li>Python 3.</li>
                <li>Tkinter library (typically pre-installed with Python)</li>
            </ul>
      </li>
      <li><b>Search and Replace:</b>
            <ul>
                <li><code>git clone https://github.com/yourusername/fusion-reactor-gui.git
cd fusion-reactor-gui</code></li>
            </ul>
      </li>
      <li><b>Run the Program:</b>
            <ul>
                <li><code>python3 fusion_gui.py</code></li>
            </ul>
      </li> 
</ul>
<h2>Usage Instructions</h2>
<h4>Main Menu</h4>
Once the GUI starts, you'll see a menu bar at the top of the window. Here's what each menu option provides:
<li><b>File:</b>
<ul>
              <li><code>Open</code>: Opens an existing input file.</li>
              <li><code>Save</code>: Saves the current configuration.</li>
              <li><code>Save As</code>: Saves the current configuration under a new file name.</li>
              <li><code>Search and Replace</code>: Opens a window to search for specific text and optionally replace it in the main text box.</li>
              <li><code>Exit</code>: Closes the application.</li>
</ul>
<li><b>Figure-of-Merit:</b>
<ul>
              <li>Opens a checkbox window to select the desired Figures-of-Merit (FoM).</li>
</ul>
<li><b>Constraint:</b>
<ul>
              <li>Opens a window to select constraint values.</li>
</ul>
<li><b>Iteration:</b>
<ul>
              <li>Opens a window to choose iteration options.</li>
</ul>
<li><b>Figure-of-Merit:</b>
<ul>
<li><b>1D:</b>
<ul>
              <li>Select a parameter to sweep and enter the values as a comma-separated list..</li>
</ul>
<li><b>2D:</b>
<ul>
              <li>Choose two parameters to sweep in 2D and enter the values for both as comma-separated lists.</li>
</ul>
  <ul>
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
