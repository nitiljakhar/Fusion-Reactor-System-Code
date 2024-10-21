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
                <li><code>git clone https://github.com/nitiljakhar/Fusion-Reactor-System-Code.git
cd Fusion-Reactor-System-Code</code></li>
            </ul>
      </li>
      <li><b>Run the Program:</b>
            <ul>
                <li><code>python3 System_code.py</code></li>
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

<h4>Scan Module</h4>
This menu handles sweeping parameters for 1D and 2D scans:
<li><b>1D:</b>
<ul>
              <li>Select a parameter to sweep and enter the values as a comma-separated list.</li>
</ul>
<li><b>2D:</b>
<ul>
              <li>Choose two parameters to sweep in 2D and enter the values for both as comma-separated lists.</li>
</ul>

<h4>Variable Selection (Various Modules)</h4>
The menu also offers various categories to select from:
<li><b>Build:</b>
<ul>
              <li>Opens a menu to select variables related to the build process.</li>
</ul>
<li><b>Constraint Variables:</b>
<ul>
              <li>Choose constraints for the fusion reactor setup.</li>
</ul>
<li><b>Cost Variables:</b>
<ul>
              <li>Manage cost-related parameters.</li>
</ul>
<li><b>Current Drive:</b>
<ul>
              <li>Select options for the current drive system.</li>
</ul>
<li><b>Divertor Variables:</b>
<ul>
              <li>Configure the divertor subsystem settings.</li>
</ul>
<li><b>Fwbs Variables:</b>
<ul>
              <li>Handle first wall and blanket structure values.</li>
</ul>
<li><b>Heat Transport:</b>
<ul>
              <li>Control heat transport-related settings.</li>
</ul>
<li><b>Impurity Radiation:</b>
<ul>
              <li>Set parameters for impurity radiation in the plasma.</li>
</ul>
<li><b>Numerics:</b>
<ul>
              <li>Fine-tune numerical parameters for the calculations.</li>
</ul>
<li><b>CS/pfcoil Variables:</b>
<ul>
              <li>Choose settings for the Central Solenoid (CS) and poloidal field (PF) coils.</li>
</ul>
<li><b>Physics Variables:</b>
<ul>
              <li>Adjust key physics variables affecting the fusion reactor.</li>
</ul>
<li><b>Pulse Variables:</b>
<ul>
              <li>Manage pulse-related values.</li>
</ul>
<li><b>Tfcoil Variables:</b>
<ul>
              <li>Set parameters for the toroidal field (TF) coil.</li>
</ul>

<h4>Text Box and Scrollbar</h4>
The main area is a text box where:
<li>The results of your selections will appear.</li>
<li>You can manually enter or modify text.</li>
<li>A vertical scrollbar allows you to navigate the content easily.</li>

<h4>Footer Buttons</h4>
<li><code>Execute</code>: Executes the DAT file in WSl Command (f'process -i "{file_name}"') .</li>
<li><code>Summary</code>: Executes WSl Command (f'./plot_proc.py -f "{file_name}_MFILE.DAT"') to open the summery document of the "Execute" command outcomes.</li>


<h2>Detailed Features</h2>
<b>Checkbox Windows</b>
<li>Each window, such as for Figures-of-Merit or Constraints, provides a list of checkboxes. You can select or deselect parameters, and the state will be retained when reopening the windows.</li>
<b>Dynamic Updates</b>
<li>The application automatically keeps track of selected options and updates them based on the current state of the main text box. This prevents inconsistencies between what is displayed and what is selected.</li>

<b>Search and Replace</b><br>
The program offers a search and replace feature to quickly modify parameters within the main text area:
<li><code>Find</code>: Highlights all instances of the searched word.</li>
<li><code>Replace</code>: Replaces all occurrences of the searched word with the new word.</li>

<h2>Customization</h2>
<li>To add more Figures of Merit, Constraints, or other parameters, update the respective dictionaries in the code. For example, to add a new constraint, modify the <code>constraint_values</code> dictionary inside <code>Constraint_checkboxes()</code>.</li>

<h2>Shortcuts</h2>
<li><code>Ctrl + F</code>: Opens the search window to find text in the main text box.</li>
<li><code>Ctrl + H</code>: Opens the replace window to find and replace text.</li>


<h2>Contributing</h2>
Feel free to fork the repository, make modifications, and send a pull request. Contributions are welcome!

<h2>License</h2>
This project is licensed under the MIT License.

<h2>Founder</h2>
<b>Nitil Jakhar</b><br>
<b><code>E-mail</code>: nitiljakhar1904jacs@gmail.com</b><br>
<b>Computer Science Engineer</b><br>
<b>Chandigarh University, Mohali, India</b><br>
