import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import os

from tkinter import filedialog, Text, messagebox, simpledialog, ttk
import subprocess
import threading

#Functionalits of File Command
#Save File Command Function
def save():
    global current_file_path
    data = text_box.get("1.0", tk.END).strip()
    if data:
        if current_file_path:
            save_to_path(current_file_path)
        else:
            save_as()
    else:
        messagebox.showwarning("Empty Input", "Please enter some data to save.")
#Save_as Command Function
def save_as():
    global current_file_path
    file_path = filedialog.asksaveasfilename(defaultextension=".DAT", filetypes=[("DAT files", "*.DAT")])
    if file_path:
        file_dir, file_name = os.path.split(file_path)
        file_name_without_ext, file_ext = os.path.splitext(file_name)
        new_file_name = f"{file_name_without_ext}_IN{file_ext}"
        new_file_path = os.path.join(file_dir, new_file_name)
        save_to_path(new_file_path)
    else:
        messagebox.showwarning("Cancelled", "Save operation cancelled.")
#Save file fath Function Specifications 
def save_to_path(path):
    global current_file_path
    data = text_box.get("1.0", tk.END).strip()
    with open(path, 'w') as file:
        file.write(data)
    current_file_path = path
    messagebox.showinfo("Success", f"Data saved successfully to {current_file_path}!")
#Open File command 
def open_file():
    global current_file_path
    file_path = filedialog.askopenfilename(filetypes=[("DAT files", "*.DAT"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'r') as file:
            data = file.read()
        
        text_box.delete("1.0", tk.END)  # Clear previous content
        text_box.insert(tk.END, data)
        current_file_path = file_path
    else:
        messagebox.showwarning("Cancelled", "Open operation cancelled.")

def toggle_night_mode():
    """Toggle between light and night mode."""
    global night_mode
    if night_mode:
        root.config(bg="white")
        text_box.config(bg="white", fg="black", insertbackground="black")
        night_mode = False
    else:
        root.config(bg="black")
        text_box.config(bg="black", fg="white", insertbackground="white")
        night_mode = True

def undo_action():
    
        text_box.edit_undo()

def redo_action():
    
        text_box.edit_redo()

def find_text():
    """Find text in the text box."""
    search_term = simpledialog.askstring("Find", "Enter text to find:")
    if search_term:
        start = text_box.search(search_term, 1.0, stopindex=tk.END)
        if start:
            end = f"{start}+{len(search_term)}c"
            text_box.tag_add("highlight", start, end)
            text_box.tag_config("highlight", background="yellow", foreground="black")
            text_box.mark_set("insert", start)
            text_box.see(start)
        else:
            messagebox.showinfo("Find", "Text not found.")

def find_and_replace():
    """Find and replace text in the text box."""
    search_term = simpledialog.askstring("Find and Replace", "Enter text to find:")
    replace_term = simpledialog.askstring("Find and Replace", "Enter replacement text:")
    if search_term and replace_term:
        content = text_box.get(1.0, tk.END)
        new_content = content.replace(search_term, replace_term)
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, new_content)

def zoom_in():
    """Increase the font size in the text box."""
    current_font_size = text_box.cget("font").split()[1]
    new_size = int(current_font_size) + 2
    text_box.config(font=("Arial", new_size))

def zoom_out():
    """Decrease the font size in the text box."""
    current_font_size = text_box.cget("font").split()[1]
    new_size = max(int(current_font_size) - 2, 8)
    text_box.config(font=("Arial", new_size))


# Unified state tracking for all checkboxes (FOM, Constraints, and others)
checkbox_states = {
    'FOM': {},
    'Constraint': {},
    'Iteration' : {},
    'Build' : {},
    'Constraint_variable' : {},
    'Cost_variables' : {},
    'Current_drive' : {},
    'Divertor_values' : {},
    'Fwbs' : {},
    'Heat_transport' : {}, 
    'IR' : {},
    'Numerics' : {},
    'CS_pf' : {},
    'Physics' : {},
    'Pulse' : {}, 
    'Tf_coil': {},
}



def execute_command():
    global current_file_path
    # Save the file (assuming `save_to_path` is defined elsewhere)
    save_to_path(current_file_path)

    # Create a new window for displaying messages
    custom_box = tk.Toplevel()
    custom_box.title("Command Execution")
    
    # Create a ScrolledText widget that expands and fills the window
    text_area = ScrolledText(custom_box, wrap=tk.WORD, width=120, height=30)
    text_area.config(state=tk.NORMAL)  # Make the text writable so we can insert output
    text_area.pack(padx=10, pady=10, expand=True, fill='both')  # Allow the text area to expand and fill the window

    # Placeholder message variable or calculate based on actual content
    message = "Example"  # You should replace this with actual content length or use a default value

    if current_file_path:
        # Extracting just the file name from the current file path
        file_name = os.path.basename(current_file_path)
        
        # Command to execute, using WSL
        command = f'process -i "{file_name}"'

        # Create a function to update the text area with new output
        def update_output(output):
            text_area.config(state=tk.NORMAL)  # Make the text_area writable
            text_area.insert(tk.END, output)
            text_area.config(state=tk.DISABLED)  # Make the text_area read-only again
            text_area.yview(tk.END)  # Scroll to the end to show the latest output
            custom_box.update_idletasks()  # Ensure the UI updates immediately

        # Function to display the close button after execution
        def display_close_button():
            close_button = tk.Button(custom_box, text="Close", command=custom_box.destroy, padx=10, pady=5, bg="red", fg="white")
            close_button.pack(pady=10, side=tk.BOTTOM)  # Add the button to the footer

        # Open command prompt and execute the command in WSL
        try:
            # Using subprocess.Popen to stream output
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Read output line by line and update the text_area
            for line in iter(process.stdout.readline, ''):
                update_output(line)

            # Wait for the process to complete and capture any remaining output
            process.stdout.close()
            process.wait()
            remaining_error = process.stderr.read()
            if remaining_error:
                update_output(f"Errors:\n{remaining_error}")

            # Display the close button after execution is complete
            display_close_button()

        except Exception as e:
            update_output(f"An unexpected error occurred: {e}\n")
            display_close_button()

    else:
        messagebox.showwarning("No File", "No file is currently open or saved.")

def summary_command():
    global current_file_path
    
    # Create a new window for displaying messages
    custom_box = tk.Toplevel()
    
    # Create a ScrolledText widget that expands and fills the window
    text_area = ScrolledText(custom_box, wrap=tk.WORD, width=120, height=30)
    text_area.config(state=tk.NORMAL)  # Make the text writable so we can insert output
    text_area.pack(padx=10, pady=10, expand=True, fill='both')  # Allow the text area to expand and fill the window

    # Placeholder message variable or calculate based on actual content
    message = "Example"  # You should replace this with actual content length or use a default value
    def show_result():
        if current_file_path:
            # Extracting the file name from the current file path
            file_name_with_extension = os.path.basename(current_file_path)

            # Removing '_IN.DAT' from the file name
            file_name = file_name_with_extension.replace('_IN.DAT', '')

            # Command to execute using WSL
            command = f'evince "{file_name}_MFILE.DATSUMMARY.pdf"'
            
            # Execute the command
            try:
                subprocess.Popen(command, shell=True)
            except Exception as e:
                update_output(f"Failed to open result file: {e}\n")
       
    Result_button = tk.Button(custom_box, text="Show Result", command=show_result)
    Result_button.pack(side="right", padx=10, pady=10)



    if current_file_path:
        # Extracting the file name from the current file path
        file_name_with_extension = os.path.basename(current_file_path)

        # Removing '_IN.DAT' from the file name
        file_name = file_name_with_extension.replace('_IN.DAT', '')

        # Command to execute, using WSL
        command = f'./plot_proc.py -f "{file_name}_MFILE.DAT"'

        # Create a function to update the text area with new output
        def update_output(output):
            text_area.config(state=tk.NORMAL)  # Make the text_area writable
            text_area.insert(tk.END, output)
            text_area.config(state=tk.DISABLED)  # Make the text_area read-only again
            text_area.yview(tk.END)  # Scroll to the end to show the latest output
            custom_box.update_idletasks()  # Ensure the UI updates immediately

        # Open command prompt and execute the command in WSL
        try:
            # Using subprocess.Popen to stream output
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Read output line by line and update the text_area
            for line in iter(process.stdout.readline, ''):
                update_output(line)

            # Wait for the process to complete and capture any remaining output
            process.stdout.close()
            process.wait()
            remaining_error = process.stderr.read()
            if remaining_error:
                update_output(f"Errors:\n{remaining_error}")

        except Exception as e:
            update_output(f"An unexpected error occurred: {e}\n")
    else:
        messagebox.showwarning("No File", "No file is currently open or saved.")

def toggle_figure(value, var, state_dict):
    cursor_index = text_box.index(tk.INSERT)
    if var.get():
        text_box.insert(cursor_index, value + "\n")
        state_dict[value] = True  # Mark as selected
    else:
        start_index = text_box.search(value, "1.0", tk.END)
        if start_index:
            end_index = f"{start_index}+{len(value)+1}c"
            text_box.delete(start_index, end_index)
        state_dict[value] = False  # Mark as deselected

#About the GUI
def show_info():
    """Function to display the message when 'i' button is clicked."""
    def open_link():
        webbrowser.open("https://github.com/nitiljakhar/Fusion-Reactor-System-Code")  # Replace with your desired URL

    # Create a popup window
    popup = tk.Toplevel()
    popup.title("Information")
    popup.geometry("300x200")  # Adjust the size of the popup

    # Make the popup a child window of the main GUI window
    popup.transient(root)  # Attach popup to the root window
    popup.grab_set()  # Block interaction with the root window until popup is closed
    popup.attributes("-topmost", False)  # Keep it on top of the GUI, but not above other apps


    # Center the popup window on the screen
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    window_width = 300
    window_height = 200
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    popup.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Add label with text wrapping (wraplength limits the text width to fit within the popup window)
    label = tk.Label(
        popup,
        text="This Python program provides a graphical user interface (GUI) to manage a fusion reactor system code PROCESS. The GUI simplifies the management of fusion reactor parameters, making the process faster and more accessible.",
        font=("Arial", 12),
        wraplength=280,  # Adjust to fit within the popup window
        justify="center"  # Align text to the left
    )
    label.pack(pady=10, padx=10)

    # Add a clickable link
    link = tk.Label(
        popup,
        text="Visit for more information",
        font=("Arial", 10, "underline"),
        fg="blue",
        cursor="hand2",
    )
    link.pack(pady=5)
    link.bind("<Button-1>", lambda e: open_link())

    # Add close button
    close_button = tk.Button(popup, text="Close", command=popup.destroy)
    close_button.pack(pady=10)
    
def create_checkboxes(window_title, value_dict, state_key):
    """Generic function to create a checkbox window, supporting submenus displayed inline."""
    checkbox_window = tk.Toplevel(root)
    checkbox_window.title(window_title)
    checkbox_window.geometry("500x400")

    # Make the pop-up modal
    checkbox_window.transient(root)  # Associate pop-up with the main window
    checkbox_window.grab_set()  # Disable interaction with the main window

    # Center the checkbox window on the screen
    screen_width = checkbox_window.winfo_screenwidth()
    screen_height = checkbox_window.winfo_screenheight()
    window_width = 500
    window_height = 400
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    checkbox_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    canvas = tk.Canvas(checkbox_window)
    scrollbar = tk.Scrollbar(checkbox_window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    state_dict = checkbox_states[state_key]  # Get the state dictionary for the current set

    for key, value in sorted(value_dict.items()):
        if isinstance(value, dict):
            # This is a submenu, create a label for the submenu title
            label = tk.Label(scrollable_frame, text=key, font=("Arial", 10, "bold"))
            label.pack(anchor="w")

            # Now create checkboxes for the submenu items
            for subkey, subvalue in sorted(value.items()):
                var = tk.BooleanVar(value=state_dict.get(subvalue, False))  # Retain previous state for submenu
                checkbox = tk.Checkbutton(scrollable_frame, text=subkey, variable=var,
                                          command=lambda v=subvalue, var=var: toggle_figure(v, var, state_dict))
                checkbox.pack(anchor="w", padx=20)  # Indent submenu checkboxes
        else:
            # This is a regular checkbox item
            var = tk.BooleanVar(value=state_dict.get(value, False))  # Retain previous state
            checkbox = tk.Checkbutton(scrollable_frame, text=key, variable=var,
                                      command=lambda v=value, var=var: toggle_figure(v, var, state_dict), font=("Arial", 10, "bold"))
            checkbox.pack(anchor="w")

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

#Figure of merits Key and values
def FOM():
    figure_values = {
        "Minimize plasma major radius": "minmax = 1 *Minimize plasma major radius", # Figure of merits
        "Minimize neutron wall load": "minmax = 3 *Minimize neutron wall load", # Figure of merits
        "Minimize total TF coil + PF coil power": "minmax = 4 *Minimize total TF coil + PF coil power", # Figure of merits
        "Minimize ratio of fusion power to injection power (Q)": "minmax = 5 *Minimize ratio of fusion power to injection power (Q)", # Figure of merits
        "Minimize cost of electricity": "minmax = 6 *Minimize cost of electricity", # Figure of merits
        "Minimize direct cost if ireactor = 0, constructed cost otherwise": "minmax = 7 *Minimize direct cost if ireactor = 0, constructed cost otherwise", # Figure of merits
        "Minimize aspect ratio": "minmax = 8 *Minimize aspect ratio", # Figure of merits
        "Minimize divertor heat load": "minmax = 9 *Minimize divertor heat load", # Figure of merits
        "Minimize toroidal field on axis": "minmax = 10 *Minimize toroidal field on axis", # Figure of merits
        "Minimize injection power": "minmax = 11 *Minimize injection power", # Figure of merits
        "Minimize pulse length": "minmax = 14 *Minimize pulse length", # Figure of merits
        "Minimize plant availability factor (N.B. requires iavail>=1)": "minmax = 15 *Minimize plant availability factor (N.B. requires iavail>=1)", # Figure of merits
        "Minimize R0 and maximize burn time (linear combination)": "minmax = 16 *Minimize R0 and maximize burn time (linear combination)", # Figure of merits
        "Minimize net electrical power": "minmax = 17 *Minimize net electrical power", # Figure of merits
        "Maximize plasma major radius": "minmax = -1 *Maximize plasma major radius", # Figure of merits
        "Maximize neutron wall load": "minmax = -3 *Maximize neutron wall load", # Figure of merits
        "Maximize total TF coil + PF coil power": "minmax = -4 *Maximize total TF coil + PF coil power", # Figure of merits
        "Maximize ratio of fusion power to injection power (Q)": "minmax = -5 *Maximize ratio of fusion power to injection power (Q)", # Figure of merits
        "Maximize cost of electricity": "minmax = -6 *Maximize cost of electricity", # Figure of merits
        "Maximize direct cost if ireactor = 0, constructed cost otherwise": "minmax = -7 *Maximize direct cost if ireactor = 0, constructed cost otherwise", # Figure of merits
        "Maximize aspect ratio": "minmax = -8 *Maximize aspect ratio", # Figure of merits
        "Maximize divertor heat load": "minmax = -9 *Maximize divertor heat load", # Figure of merits
        "Maximize toroidal field on axis": "minmax = -10 *Maximize toroidal field on axis", # Figure of merits
        "Maximize injection power": "minmax = -11 *Maximize injection power", # Figure of merits
        "Maximize pulse length": "minmax = -14 *Maximize pulse length", # Figure of merits
        "Maximize plant availability factor (N.B. requires iavail>=1)": "minmax = -15 *Maximize plant availability factor (N.B. requires iavail>=1)", # Figure of merits
        "Maximize R0 and maximize burn time (linear combination)": "minmax = -16 *Maximize R0 and maximize burn time (linear combination)", # Figure of merits
        "Maximize net electrical power": "minmax = -17 *Maximize net electrical power", # Figure of merits
        "No FOM": "minmax = 18 *No FOM", # Figure of merits
        "Linear combination of big Q and pulse length (maximized)": "minmax = -19 *Linear combination of big Q and pulse length (maximized)", # Figure of merits
    }
    create_checkboxes("Select Figures-of-Merit", figure_values, 'FOM')

#FConstraint Key and values
def Constraint():
    constraint_values = {
        "Beta (itv 5)": "icc = 1 *Beta (itv 5)", # Constraints
        "Global power balance (itv 10,1,2,3,4,6,11)": "icc = 2 *Global power balance (itv 10,1,2,3,4,6,11)", # Constraints
        "Density upper limit (itv 9,1,2,3,4,5,6)": "icc = 5 *Density upper limit (itv 9,1,2,3,4,5,6)", # Constraints
        "Epsilon-beta poloidal upper limit (itv 8,1,2,3,4,6)": "icc = 6 *Epsilon-beta poloidal upper limit (itv 8,1,2,3,4,6)", # Constraints
        "Beam ion density (NBI) (itv 7)": "icc = 7 *Beam ion density (NBI) (itv 7)", # Constraints
        "Neutron wall load upper limit (itv 14,1,2,3,4,6)": "icc = 8 *Neutron wall load upper limit (itv 14,1,2,3,4,6)", # Constraints
        "Fusion power upper limit (itv 26,1,2,3,4,6)": "icc = 9 *Fusion power upper limit (itv 26,1,2,3,4,6)", # Constraints
        "Toroidal field 1/R consistency (itv 12,1,2,3,13)": "icc = 10 *Toroidal field 1/R consistency (itv 12,1,2,3,13)", # Constraints
        "Radial build consistency (itv 3,1,13,16,29,42,61)": "icc = 11 *Radial build consistency (itv 3,1,13,16,29,42,61)", # Constraints
        "Volt-second lower limit (STEADY STATE) (itv 15,1,2,3)": "icc = 12 *Volt-second lower limit (STEADY STATE) (itv 15,1,2,3)", # Constraints
        "Burn time lower limit (Pulse) (itv 21,1,16,17,29,42,44,61)": "icc = 13 *Burn time lower limit (Pulse) (itv 21,1,16,17,29,42,44,61)", # Constraints
        "Neutral beam decay lengths = tbeamin consistency (NBI) (itv 19,1,2,3,6)": "icc = 14 *Neutral beam decay lengths = tbeamin consistency (NBI) (itv 19,1,2,3,6)", # Constraints
        "LH power threshold limit (itv 103)": "icc = 15 *LH power threshold limit (itv 103)", # Constraints
        "Net electric power lower limit (itv 25,1,2,3)": "icc = 16 *Net electric power lower limit (itv 25,1,2,3)", # Constraints
        "Radiation fraction upper limit (itv 28)": "icc = 17 *Radiation fraction upper limit (itv 28)", # Constraints
        "Divertor heat load upper limit (itv 28)": "icc = 18 *Divertor heat load upper limit (itv 28)", # Constraints
        "MVA upper limit (total power consumption during a pulse) (itv 30)": "icc = 19 *MVA upper limit (total power consumption during a pulse) (itv 30)", # Constraints
        "Neutral beam tangency radius upper limit (NBI) (itv 33,31,3,13)": "icc = 20 *Neutral beam tangency radius upper limit (NBI) (itv 33,31,3,13)", # Constraints
        "Minor radius lower limit (itv 32)": "icc = 21 *Minor radius lower limit (itv 32)", # Constraints
        "Divertor collisionality upper limit (itv 34,43)": "icc = 22 *Divertor collisionality upper limit (itv 34,43)", # Constraints
        "Conducting shell to plasma minor radius ratio upper limit (itv 104,1,74)": "icc = 23 *Conducting shell to plasma minor radius ratio upper limit (itv 104,1,74)", # Constraints
        "Beta upper limit (itv 36,1,2,3,4,6,18)": "icc = 24 *Beta upper limit (itv 36,1,2,3,4,6,18)", # Constraints
        "Peak toroidal field upper limit (itv 35,3,13,29)": "icc = 25 *Peak toroidal field upper limit (itv 35,3,13,29)", # Constraints
        "Central solenoid EOF current density upper limit (ipfres=0) (itv 38,37,41,12)": "icc = 26 *Central solenoid EOF current density upper limit (ipfres=0) (itv 38,37,41,12)", # Constraints
        "Central solenoid BOP current density upper limit (ipfres=0) (itv 39,37,41,12)": "icc = 27 *Central solenoid BOP current density upper limit (ipfres=0) (itv 39,37,41,12)", # Constraints
        "Fusion gain Q lower limit (itv 45,47,40)": "icc = 28 *Fusion gain Q lower limit (itv 45,47,40)", # Constraints
        "Inboard radial build consistency (itv 3,1,13,16,29,42,61)": "icc = 29 *Inboard radial build consistency (itv 3,1,13,16,29,42,61)", # Constraints
        "Injection power upper limit (itv 46,47,11)": "icc = 30 *Injection power upper limit (itv 46,47,11)", # Constraints
        "TF coil case stress upper limit (SCTF) (itv 48,56,57,58,59,60,24)": "icc = 31 *TF coil case stress upper limit (SCTF) (itv 48,56,57,58,59,60,24)", # Constraints
        "TF coil conduit stress upper limit (SCTF) (itv 49,56,57,58,59,60,24)": "icc = 32 *TF coil conduit stress upper limit (SCTF) (itv 49,56,57,58,59,60,24)", # Constraints
        "I_op / I_critical (TF coil) (SCTF) (itv 50,56,57,58,59,60,24)": "icc = 33 *I_op / I_critical (TF coil) (SCTF) (itv 50,56,57,58,59,60,24)", # Constraints
        "Dump voltage upper limit (SCTF) (itv 51,52,56,57,58,59,60,24)": "icc = 34 *Dump voltage upper limit (SCTF) (itv 51,52,56,57,58,59,60,24)", # Constraints
        "J_winding pack/J_protection upper limit (SCTF) (itv 53,56,57,58,59,60,24)": "icc = 35 *J_winding pack/J_protection upper limit (SCTF) (itv 53,56,57,58,59,60,24)", # Constraints
        "TF coil temperature margin lower limit (SCTF) (itv 54,55,56,57,58,59,60,24)": "icc = 36 *TF coil temperature margin lower limit (SCTF) (itv 54,55,56,57,58,59,60,24)", # Constraints
        "Current drive gamma upper limit (itv 40,47)": "icc = 37 *Current drive gamma upper limit (itv 40,47)", # Constraints
        "First wall coolant temperature rise upper limit (PULSE) (itv 62)": "icc = 38 *First wall coolant temperature rise upper limit (PULSE) (itv 62)", # Constraints
        "First wall peak temperature upper limit (PULSE)": "icc = 39 *First wall peak temperature upper limit (PULSE)", # Constraints
        "Central solenoid stored energy lower limit (SCTF)": "icc = 41 *Central solenoid stored energy lower limit (SCTF)", # Constraints
        "Combined stress upper limit on winding pack (SCTF)": "icc = 42 *Combined stress upper limit on winding pack (SCTF)", # Constraints
        "TF bundle vertical stress upper limit (SCTF)": "icc = 43 *TF bundle vertical stress upper limit (SCTF)", # Constraints
        "Total cost upper limit": "icc = 44 *Total cost upper limit", # Constraints
        "Edge safety factor lower limit (ST)": "icc = 45 *Edge safety factor lower limit (ST)", # Constraints
        "Ip/Irod upper limit (ST)": "icc = 46 *Ip/Irod upper limit (ST)", # Constraints
        "TF coil toroidal thickness upper limit (RFP)": "icc = 47 *TF coil toroidal thickness upper limit (RFP)", # Constraints
        "Poloidal beta upper limit": "icc = 48 *Poloidal beta upper limit", # Constraints
        "Reversal parameter < 0 (RFP)": "icc = 49 *Reversal parameter < 0 (RFP)", # Constraints
        "IFE repetition rate upper limit (IFE)": "icc = 50 *IFE repetition rate upper limit (IFE)", # Constraints
        "Startup volt-seconds consistency (PULSE)": "icc = 51 *Startup volt-seconds consistency (PULSE)", # Constraints
        "Tritium breeding ratio lower limit": "icc = 52 *Tritium breeding ratio lower limit", # Constraints
        "Peak neutron fluence on TF coil upper limit": "icc = 53 *Peak neutron fluence on TF coil upper limit", # Constraints
        "Peak TF coil nuclear heating upper limit": "icc = 54 *Peak TF coil nuclear heating upper limit", # Constraints
        "Final He concentration in vacuum vessel upper limit": "icc = 55 *Final He concentration in vacuum vessel upper limit", # Constraints
        "Pseparatrix/Rmajor upper limit": "icc = 56 *Pseparatrix/Rmajor upper limit", # Constraints
        "Neutral beam shine-through fraction upper limit (NBI)": "icc = 59 *Neutral beam shine-through fraction upper limit (NBI)", # Constraints
        "Central solenoid temperature margin lower limit (SCTF)": "icc = 60 *Central solenoid temperature margin lower limit (SCTF)", # Constraints
        "Minimum availability value limit": "icc = 61 *Minimum availability value limit", # Constraints
        "Lower limit on the ratio of alpha particle to energy confinement times": "icc = 62 *Lower limit on the ratio of alpha particle to energy confinement times", # Constraints
        "Number of vacuum pumps (vacuum model=simple)": "icc = 63 *Number of vacuum pumps (vacuum model=simple)", # Constraints
        "Limit on Zeff ≤ Zeffmax": "icc = 64 *Limit on Zeff ≤ Zeffmax", # Constraints
        "TF dump time greater than or equal to calculated quench time": "icc = 65 *TF dump time greater than or equal to calculated quench time", # Constraints
        "Limit on rate of change of energy in poloidal field": "icc = 66 *Limit on rate of change of energy in poloidal field", # Constraints
        "Pseparatrix Bt / q A": "icc = 68 *Pseparatrix Bt / q A", # Constraints
        "Central solenoid shear stress limit (Tresca yield criterion)": "icc = 72 *Central solenoid shear stress limit (Tresca yield criterion)", # Constraints
        "Neped<ne0": "icc = 81 *Neped<ne0", # Constraints
    }
    create_checkboxes("Select Constraint Value", constraint_values, 'Constraint')

#Ietarion Function Encapsule
def Iteration():
    """Display a list of checkboxes for the user to select Iteration, with a scrollbar."""
    Iteration_values = {
        "aspect ratio": "ixc = 1 *aspect \nboundu(1)=10.00D0 \nboundl(1)=1.100D0", #Iterations 
        "bt": "ixc = 2 *bt \nboundu(2)=30.00D0 \nboundl(2)=0.010D0", #Iterations
        "rmajor": "ixc = 3 *rmajor \nboundu(3)=50.00D0 \nboundl(3)=0.100D0", #Iterations
        "te": "ixc = 4 *te \nboundu(4)=150.0D0 \nboundl(4)=5.000D0", #Iterations
        "beta": "ixc = 5 *beta \nboundu(5)=1.000D0 \nboundl(5)=0.001D0", #Iterations
        "dene": "ixc = 6 *dene \nboundu(6)=1.00D21 \nboundl(6)=1.00D19", #Iterations
        "(rnbeam) hot beam density / electron density": "ixc = 7 *(rnbeam) hot beam density / electron density \nboundu(7)=1.000D0 \nboundl(7)=1.00D-6", #Iterations
        "(fbeta) f-value for epsilon.βp limit equation": "ixc = 8 *(fbeta) f-value for epsilon.βp limit equation \nboundu(8)=1.000D0 \nboundl(8)=0.001D0", #Iterations
        "(fdene) f-value for density limit equation ": "ixc = 9 *(fdene) f-value for density limit equation  \nboundu(9)=1.000D0 \nboundl(9)=0.001D0", #Iterations
        "(hfact) confinement time H-factor": "ixc = 10 *(hfact) confinement time H-factor \nboundu(10)=3.000D0 \nboundl(10)=0.100D0", #Iterations
        "(pheat) heating power not used for current drive ": "ixc = 11 *(pheat) heating power not used for current drive  \nboundu(11)=1.000D3 \nboundl(11)=1.00D-3", #Iterations
        "(oacdcp) overall current density in TF coil inboard leg": "ixc = 12 *(oacdcp) overall current density in TF coil inboard leg \nboundu(12)=1.500D8 \nboundl(12)=1.000D5", #Iterations
        "(tfcth) TF coil inboard leg thickness ": "ixc = 13 *(tfcth) TF coil inboard leg thickness  \nboundu(13)=5.000D0 \nboundl(13)=0.100D0", #Iterations
        "(fwalld) f-value for wall load limit equation": "ixc = 14 *(fwalld) f-value for wall load limit equation \nboundu(14)=5.000D0 \nboundl(14)=0.001D0", #Iterations
        "(fvs) f-value for volt second limit equation": "ixc = 15 *(fvs) f-value for volt second limit equation \nboundu(15)=10.000 \nboundl(15)=0.001D0", #Iterations
        "(ohcth) central solenoid thickness ": "ixc = 16 *(ohcth) central solenoid thickness  \nboundu(16)=10.00D0 \nboundl(16)=0.010D0", #Iterations
        "(tdwell) dwell time": "ixc = 17 *(tdwell) dwell time \nboundu(17)=1.000D8 \nboundl(17)=0.100D0", #Iterations
        "(q) edge safety factor ": "ixc = 18 *(q) edge safety factor  \nboundu(18)=50.00D0 \nboundl(18)=2.000D0", #Iterations
        "(enbeam) neutral beam energy": "ixc = 19 *(enbeam) neutral beam energy \nboundu(19)=1.000D6 \nboundl(19)=1.000D0", #Iterations
        "(tcpav) average (resistive) TF coil temperature for ST only": "ixc = 20 *(tcpav) average (resistive) TF coil temperature for ST only \nboundu(20)=3.000D2 \nboundl(20)=40.00D0", #Iterations
        "(ftburn) f-value for burn time limit equation": "ixc = 21 *(ftburn) f-value for burn time limit equation \nboundu(21)=1.000D0 \nboundl(21)=0.001D0", #Iterations
        "(fcoolcp) coolant fraction of resistive TF coil": "ixc = 23 *(fcoolcp) coolant fraction of resistive TF coil \nboundu(23)=0.500D0 \nboundl(23)=0.100D0", #Iterations
        "(cdtfleg) TF coil leg overall current density": "ixc = 24 *(cdtfleg) TF coil leg overall current density \nboundu(6)=6.0 \nboundl(6)=", #Iterations
        "(fpnetel) f-value for net electric power limit equation": "ixc = 25 *(fpnetel) f-value for net electric power limit equation \nboundu(25)=1.000D0 \nboundl(25)=0.001D0", #Iterations
        "(ffuspow) f-value for fusion power limit equation": "ixc = 26 *(ffuspow) f-value for fusion power limit equation \nboundu(26)=1.000D0 \nboundl(26)=0.001D0", #Iterations
        "(fhldiv) f-value for divertor heat load limit equation": "ixc = 27 *(fhldiv) f-value for divertor heat load limit equation \nboundu(27)=1.000D0 \nboundl(27)=0.001D0", #Iterations
        "(fradpwr) f-value for radiation power limit equation ": "ixc = 28 *(fradpwr) f-value for radiation power limit equation  \nboundu(28)=0.990D0 \nboundl(28)=0.001D0", #Iterations
        "(bore) machine bore ": "ixc = 29 *(bore) machine bore  \nboundu(29)=10.00D0 \nboundl(29)=0.100D0", #Iterations
        "(fmva) f-value for MVA limit equation": "ixc = 30 *(fmva) f-value for MVA limit equation \nboundu(30)=1.000D0 \nboundl(30)=0.010D0", #Iterations
        "(gapomin) minimum gap between outboard vacuum vessel and TF coil": "ixc = 31 *(gapomin) minimum gap between outboard vacuum vessel and TF coil \nboundu(31)=1.000D1 \nboundl(31)=0.001D0", #Iterations
        "(frminor) f-value for minor radius limit equation": "ixc = 32 *(frminor) f-value for minor radius limit equation \nboundu(32)=1.000D0 \nboundl(32)=0.001D0", #Iterations
        "(fportsz) f-value for beam tangency radius limit equation": "ixc = 33 *(fportsz) f-value for beam tangency radius limit equation \nboundu(33)=1.000D0 \nboundl(33)=0.001D0", #Iterations
        "(fdivcol) f-value for divertor collisionality limit equation": "ixc = 34 *(fdivcol) f-value for divertor collisionality limit equation \nboundu(34)=1.000D0 \nboundl(34)=0.001D0", #Iterations
        "(fpeakb) f-value for peak toroidal field limit equation": "ixc = 35 *(fpeakb) f-value for peak toroidal field limit equation \nboundu(35)=1.000D0 \nboundl(35)=0.001D0", #Iterations
        "(fbetatry) f-value for beta limit equation": "ixc = 36 *(fbetatry) f-value for beta limit equation \nboundu(36)=1.000D0 \nboundl(36)=0.001D0", #Iterations
        "(coheof) central solenoid current density at end of flat-top ": "ixc = 37 *(coheof) central solenoid current density at end of flat-top  \nboundu(37)=1.000D8 \nboundl(37)=1.000D5", #Iterations
        "(fjohc) f-value for central solenoid current at EOF limit equation ": "ixc = 38 *(fjohc) f-value for central solenoid current at EOF limit equation  \nboundu(38)=1.000D0 \nboundl(38)=0.010D0", #Iterations
        "(fjohc0) f-value for central solenoid current at BOP limit equation ": "ixc = 39 *(fjohc0) f-value for central solenoid current at BOP limit equation  \nboundu(39)=1.000D0 \nboundl(39)=0.001D0", #Iterations
        "(fgamcd)f-value for current drive gamma limit equation": "ixc = 40 *(fgamcd)f-value for current drive gamma limit equation \nboundu(40)=1.000D0 \nboundl(40)=0.001D0", #Iterations
        "(fcohbop) central solenoid current density ratio BOP/EOF": "ixc = 41 *(fcohbop) central solenoid current density ratio BOP/EOF \nboundu(41)=1.000D0 \nboundl(41)=0.001D0", #Iterations
        "(gapoh) gap between central solenoid and TF coil ": "ixc = 42 *(gapoh) gap between central solenoid and TF coil  \nboundu(42)=10.00D0 \nboundl(42)=0.001D0", #Iterations      
        "(fvsbrnni) fraction of plasma current produced by non-inductive means ": "ixc = 44 *(fvsbrnni) fraction of plasma current produced by non-inductive means  \nboundu(44)=1.000D0 \nboundl(44)=0.001D0", #Iterations
        "(fqval) f-value for fusion gain limit equation": "ixc = 45 *(fqval) f-value for fusion gain limit equation \nboundu(45)=1.000D0 \nboundl(45)=0.001D0", #Iterations
        "(fpinj) f-value for injection power limit equation": "ixc = 46 *(fpinj) f-value for injection power limit equation \nboundu(46)=1.000D0 \nboundl(46)=0.001D0", #Iterations
        "(feffcd) current drive efficiency multiplier": "ixc = 47 *(feffcd) current drive efficiency multiplier \nboundu(47)=1.000D0 \nboundl(47)=0.001D0", #Iterations
        "(fstrcase) f-value for TF coil case stress limit equation": "ixc = 48 *(fstrcase) f-value for TF coil case stress limit equation \nboundu(48)=1.000D0 \nboundl(48)=0.001D0", #Iterations
        "(fstrcond) f-value for TF coil conduit stress limit equation": "ixc = 49 *(fstrcond) f-value for TF coil conduit stress limit equation \nboundu(49)=1.000D0 \nboundl(49)=0.001D0", #Iterations
        "(fiooic) f-value for TF coil conduit stress limit equation ": "ixc = 50 *(fiooic) f-value for TF coil conduit stress limit equation  \nboundu(50)=1.000D0 \nboundl(50)=0.001D0", #Iterations
        "(fvdump) f-value for TF coil dump voltage limit equation": "ixc = 51 *(fvdump) f-value for TF coil dump voltage limit equation \nboundu(51)=1.000D0 \nboundl(51)=0.001D0", #Iterations
        "(vdalw) allowable TF coil dump voltage ": "ixc = 52 *(vdalw) allowable TF coil dump voltage  \nboundu(52)=1.000D6 \nboundl(52)=0.001D0", #Iterations
        "(fjprot) f-value for TF coil current protection limit equation": "ixc = 53 *(fjprot) f-value for TF coil current protection limit equation \nboundu(53)=1.000D0 \nboundl(53)=0.001D0", #Iterations
        "(ftmargtf) f-value for TF coil temperature margin limit equation": "ixc = 54 *(ftmargtf) f-value for TF coil temperature margin limit equation \nboundu(54)=1.000D0 \nboundl(54)=0.001D0", #Iterations
        "(tdmptf) dump time for TF coil": "ixc = 56 *(tdmptf) dump time for TF coil \nboundu(56)=100.0D0 \nboundl(56)=0.100D0", #Iterations
        "(thkcas) TF coil external case thickness": "ixc = 57 *(thkcas) TF coil external case thickness\nboundu(57)=1.000D0 \nboundl(57)=0.050D0", #Iterations
        "(thwcndut) TF coil conduit case thickness ": "ixc = 58 *(thwcndut) TF coil conduit case thickness  \nboundu(58)=0.100D0 \nboundl(58)=0.001D0", #Iterations
        "(fcutfsu) copper fraction of cable conductor": "ixc = 59 *(fcutfsu) copper fraction of cable conductor \nboundu(59)=1.000D0 \nboundl(59)=0.001D0", #Iterations
        "(cpttf) current per turn in the TF coils ": "ixc = 60 *(cpttf) current per turn in the TF coils  \nboundu(60)=4.000D4 \nboundl(60)=0.001D0", #Iterations
        "(gapds) gap between vacuum vessel and inboard TF coil": "ixc = 61 *(gapds) gap between vacuum vessel and inboard TF coil \nboundu(61)=10.00D0 \nboundl(61)=0.001D0", #Iterations
        "fdtmp f-value for 1st wall coolant temperature rise limit equation 38 0.001D0 1.000D0": "ixc = 62 *fdtmp f-value for 1st wall coolant temperature rise limit equation 38 0.001D0 1.000D0 \nboundu(62)=1.000D0 \nboundl(62)=0.001D0", #Iterations
        "ftpeak f-value for 1st wall peak temperature limit equation 39 0.001D0 1.000D0": "ixc = 63 *ftpeak f-value for 1st wall peak temperature limit equation 39 0.001D0 1.000D0 \nboundu(63)=1.000D0 \nboundl(63)=0.001D0", #Iterations
        "fauxmn f-value for minimum auxiliary power limit equation 40 0.001D0 1.000D0": "ixc = 64 *fauxmn f-value for minimum auxiliary power limit equation 40 0.001D0 1.000D0 \nboundu(64)=1.000D0 \nboundl(64)=0.001D0", #Iterations
        "(tohs) Plasma current ramp-up time": "ixc = 65 *(tohs) Plasma current ramp-up time \nboundu(65)=1.000D3 \nboundl(65)=0.100D0", #Iterations
        "(ftohs) f-value for central solenoid current ramp-up time limit equation": "ixc = 66 *(ftohs) f-value for central solenoid current ramp-up time limit equation \nboundu(66)=1.000D0 \nboundl(66)=0.001D0", #Iterations
        "ftcycl (f-value for equation 42)": "ixc = 67 *ftcycl (f-value for equation 42) \nboundu(67)=1.000D0 \nboundl(67)=0.001D0", #Iterations
        "(fptemp) f-value for maximum centrepost temperature limit equation eqn 44": "ixc = 68 *(fptemp) f-value for maximum centrepost temperature limit equation eqn 44 \nboundu(68)= 1.000D0 \nboundl(68)=0.001D0", #Iterations
        "rcool average radius of centrepost coolant channel 0.001D0 0.010D0": "ixc = 69 *rcool average radius of centrepost coolant channel 0.001D0 0.010D0 \nboundu(69)=0.010D0 \nboundl(69)=0.001D0", #Iterations
        "vcool maximum centrepost coolant flow speed at midplane 1.000D0 1.000D2": "ixc = 70 *vcool maximum centrepost coolant flow speed at midplane 1.000D0 1.000D2 \nboundu(70)=1.000D2 \nboundl(70)=1.000D0", #Iterations
        "fq f-value for minimum edge safety factor limit equation 45 0.001D0 1.000D0": "ixc = 71 *fq f-value for minimum edge safety factor limit equation 45 0.001D0 1.000D0 \nboundu(71)=1.000D0 \nboundl(71)=0.001D0", #Iterations
        "fipir f-value for maximum Ip/Irod limit equation 46 0.001D0 1.000D0": "ixc = 72 *fipir f-value for maximum Ip/Irod limit equation 46 0.001D0 1.000D0 \nboundu(72)=1.000D0 \nboundl(72)=0.001D0", #Iterations
        "scrapli inboard gap between plasma and first wall 0.001D0 10.00D0": "ixc = 73 *scrapli inboard gap between plasma and first wall 0.001D0 10.00D0 \nboundu(73)=10.00D0 \nboundl(73)=0.001D0", #Iterations
        "scraplo outboard gap between plasma and first wall 0.001D0 10.00D0": "ixc = 74 *scraplo outboard gap between plasma and first wall 0.001D0 10.00D0 \nboundu(74)=10.00D0 \nboundl(74)=0.001D0", #Iterations
        "tfootfi ratio of TF coil outboard/inboard leg thickness 0.200D0 5.000D0": "ixc = 75 *tfootfi ratio of TF coil outboard/inboard leg thickness 0.200D0 5.000D0 \nboundu(75)=5.000D0 \nboundl(75)=0.200D0", #Iterations
        "fbetap f-value for poloidal beta limit equation 48 0.001D0 1.000D0": "ixc = 79 *fbetap f-value for poloidal beta limit equation 48 0.001D0 1.000D0 \nboundu(79)=1.000D0 \nboundl(79)=0.001D0", #Iterations
        "edrive IFE driver energy 1.000D5 5.000D7": "ixc = 81 *edrive IFE driver energy 1.000D5 5.000D7 \nboundu(81)=5.000d7 \nboundl(81)=1.000d5", #Iterations
        "drveff IFE driver wall plug to target efficiency 0.010D0 1.000D0": "ixc = 82 *drveff IFE driver wall plug to target efficiency 0.010D0 1.000D0 \nboundu(82)=1.000D0 \nboundl(82)=0.010D0", #Iterations
        "tgain IFE target gain 1.000D0 500.0D0": "ixc = 83 *tgain IFE target gain 1.000D0 500.0D0 \nboundu(83)=500.0D0 \nboundl(83)=1.000D0", #Iterations
        "chrad radius of IFE chamber 0.100D0 20.00D0": "ixc = 84 *chrad radius of IFE chamber 0.100D0 20.00D0 \nboundu(84)=20.00D0 \nboundl(84)=0.100D0", #Iterations
        "pdrive IFE driver power reaching target 1.000D6 2.000D8": "ixc = 85 *pdrive IFE driver power reaching target 1.000D6 2.000D8 \nboundu(85)=200.0D6 \nboundl(85)=1.000D6", #Iterations
        "frrmax f-value for maximum IFE repetition rate equation 50 0.001D0 1.000D0": "ixc = 86 *frrmax f-value for maximum IFE repetition rate equation 50 0.001D0 1.000D0 \nboundu(86)=1.000D0 \nboundl(86)=0.001D0", #Iterations    
        "ftbr f-value for tritium breeding ratio limit equation 52 0.001D0 1.000D0": "ixc = 89 *ftbr f-value for tritium breeding ratio limit equation 52 0.001D0 1.000D0 \nboundu(89)=1.000D0 \nboundl(89)=0.001D0", #Iterations
        "blbuith inboard blanket breeding unit thickness 0.001D0 2.000D0": "ixc = 90 *blbuith inboard blanket breeding unit thickness 0.001D0 2.000D0 \nboundu(90)=2.000D0 \nboundl(90)=0.001D0", #Iterations
        "blbuoth outboard blanket breeding unit thickness 0.001D0 2.000D0": "ixc = 91 *blbuoth outboard blanket breeding unit thickness 0.001D0 2.000D0 \nboundu(91)=2.000D0 \nboundl(91)=0.001D0", #Iterations
        "fflutf f-value for fast neutron fluence on TF coil equation 53 0.001D0 1.000D0": "ixc = 92 *fflutf f-value for fast neutron fluence on TF coil equation 53 0.001D0 1.000D0 \nboundu(92)=1.000D0 \nboundl(92)=0.001D0", #Iterations
        "shldith inboard shield thickness 0.001D0 10.00D0": "ixc = 93 *shldith inboard shield thickness 0.001D0 10.00D0 \nboundu(93)=10.00D0 \nboundl(93)=0.001D0", #Iterations
        "shldoth outboard shield thickness 0.001D0 10.00D0": "ixc = 94 *shldoth outboard shield thickness 0.001D0 10.00D0 \nboundu(94)=10.00D0 \nboundl(94)=0.001D0", #Iterations
        "fptfnuc f-value for TF coil nuclear heating limit equation 54 0.001D0 1.000D0": "ixc = 95 *fptfnuc f-value for TF coil nuclear heating limit equation 54 0.001D0 1.000D0 \nboundu(95)=1.000D0 \nboundl(95)=0.001D0", #Iterations
        "fvvhe f-value for vessel He concentration limit equation 55 0.001D0 1.000D0": "ixc = 96 *fvvhe f-value for vessel He concentration limit equation 55 0.001D0 1.000D0 \nboundu(96)=1.000D0 \nboundl(96)=0.001D0", #Iterations
        "fpsepr f-value for Pseparatrix/Rmajor limit equation 56 0.001D0 1.000D0": "ixc = 97 *fpsepr f-value for Pseparatrix/Rmajor limit equation 56 0.001D0 1.000D0 \nboundu(97)=1.000D0 \nboundl(97)=0.001D0", #Iterations
        "li6enrich lithium-6 enrichment percentage (blktmodel=1) 7.400D0 100.0D0": "ixc = 98 *li6enrich lithium-6 enrichment percentage (blktmodel=1) 7.400D0 100.0D0 \nboundu(98)=100.0D0 \nboundl(98)=10.00D0", #Iterations   
        "flhthresh f-value for L-H power threshold limit equation 15 1.000D0 1.000D6": "ixc = 103 *flhthresh f-value for L-H power threshold limit equation 15 1.000D0 1.000D6 \nboundu(103)=1.000D6 \nboundl(103)=1.000D0", #Iterations
        "fcwr f-value for conducting shell radius limit equation 23 0.001D0 1.000D0": "ixc = 104 *fcwr f-value for conducting shell radius limit equation 23 0.001D0 1.000D0 \nboundu(104)=1.000D0 \nboundl(104)=0.001D0", #Iterations
        "fnbshinef f-value for NBI shine-through fraction limit equation 59 0.001D0 1.000D0": "ixc = 105 *fnbshinef f-value for NBI shine-through fraction limit equation 59 0.001D0 1.000D0 \nboundu(105)=1.000D0 \nboundl(105)=0.001D0", #Iterations
        "ftmargoh f-value for CS coil temperature margin limit equation 60 0.001D0 1.000D0": "ixc = 106 *ftmargoh f-value for CS coil temperature margin limit equation 60 0.001D0 1.000D0 \nboundu(106)=0.001D0 \nboundl(106)=0.001D0", #Iterations
        "favail f-value for minimum availability limit equation 61 0.001D0 1.000D0": "ixc = 107 *favail f-value for minimum availability limit equation 61 0.001D0 1.000D0 \nboundu(107)=1.000D0 \nboundl(107)=0.001D0", #Iterations
        "breeder_f breeder volume ratio: Li4SiO4/(Be12Ti+Li4SiO4) 0.060D0 1.000D0": "ixc = 108 *breeder_f breeder volume ratio: Li4SiO4/(Be12Ti+Li4SiO4) 0.060D0 1.000D0 \nboundu(108)=1.000D0 \nboundl(108)=0.060D0", #Iterations
        "ralpne thermal alpha density / electron density 0.050D0 0.150D0": "ixc = 109 *ralpne thermal alpha density / electron density 0.050D0 0.150D0 \nboundu(109)=0.150D0 \nboundl(109)=0.050D0", #Iterations
        "ftaulimit f-value for limit on ratio of alpha particle to energy confinement times 62 0.001D0 1.000D0": "ixc = 110 *ftaulimit f-value for limit on ratio of alpha particle to energy confinement times 62 0.001D0 1.000D0 \nboundu(110)=1.000D0 \nboundl(110)=0.001D0", #Iterations
        "fniterpump f-value for constraint that number of pumps ¡ tfno 63 0.001D0 1.000D0": "ixc = 111 *fniterpump f-value for constraint that number of pumps ¡ tfno 63 0.001D0 1.000D0 \nboundu(111)=0.001D0 \nboundl(111)=1.000D0", #Iterations
        "fzeffmax f-value for Zeff limit equation 64 0.001D0 1.000D0": "ixc = 112 *fzeffmax f-value for Zeff limit equation 64 0.001D0 1.000D0 \nboundu(112)=1.000D0 \nboundl(112)=0.001D0", #Iterations
        "ftaucq f-value for quench time limit equation 65 0.001D0 1.000D0": "ixc = 113 *ftaucq f-value for quench time limit equation 65 0.001D0 1.000D0 \nboundu(113)=1.000D0 \nboundl(113)=0.001D0", #Iterations
        "fw channel length Length of a single first wall channel 39 0.001D0 1.000D3": "ixc = 114 *fw channel length Length of a single first wall channel 39 0.001D0 1.000D3 \nboundu(114)=1.000D3 \nboundl(114)=0.001D0", #Iterations
        "fpoloidalpower f-value for max rate of change of energy in poloidal field 66 0.001D0 1.000D0 ": "ixc = 115 *fpoloidalpower f-value for max rate of change of energy in poloidal field 66 0.001D0 1.000D0 \nboundu(115)=1.000D0 \nboundl(115)=0.001D0", #Iterations
        "fradwall: f-value for radiation wall load limit": "ixc = 116 *fradwall: f-value for radiation wall load limit \nboundu(116)=1.000D0 \nboundl(116)=0.001D0", #Iterations       
        "fpsepbqar f-value for Psep*Bt/qar upper limit (eq. 68)": "ixc = 117 *fpsepbqar f-value for Psep*Bt/qar upper limit (eq. 68) \nboundu(117)=1.000D0 \nboundl(117)=0.001D0", #Iterations
        "f-value to ensure separatrix power is less than": "ixc = 118 *f-value to ensure separatrix power is less than \nboundu(118)=1.000D0 \nboundl(118)=0.001D0", #Iterations
        "tesep:  separatrix temperature calculated by the Kallenbach divertor model": "ixc = 119 *tesep:  separatrix temperature calculated by the Kallenbach divertor model \nboundu(119)=1.000D1 \nboundl(119)=0.000D0", #Iterations       
        "ttarget: Plasma temperature adjacent to divertor sheath [eV]": "ixc = 120 *ttarget: Plasma temperature adjacent to divertor sheath [eV] \nboundu(120)=1.000D4 \nboundl(120)=1.000D0", #Iterations       
        "neratio: ratio of mean SOL density at OMP to separatrix density at OMP": "ixc = 121 *neratio: ratio of mean SOL density at OMP to separatrix density at OMP \nboundu(121)=1.000D0 \nboundl(121)=0.001D0", #Iterations
        "oh_steel_frac steel fraction of Central Solenoid": "ixc = 122 *oh_steel_frac steel fraction of Central Solenoid \nboundu(122)=0.950D0 \nboundl(122)=0.001D0", #Iterations
        "foh_stress f-value for CS coil Tresca yield criterion (f-value for eq. 72)": "ixc = 123 *foh_stress f-value for CS coil Tresca yield criterion (f-value for eq. 72) \nboundu(123)=1.000D0 \nboundl(123)=0.001D0", #Iterations
        "qtargettotal : Power density on target including surface recombination [W/m2]": "ixc = 124 *qtargettotal : Power density on target including surface recombination [W/m2] \nboundu(124)=1.000D7 \nboundl(124)=0.001D0", #Iterations
        "beryllium density fraction relative to electron density": "ixc =125  *Beryllium density fraction relative to electron density \nboundu(125)=0.010D0 \nboundl(125)=1.00D-8", #Iterations
        "carbon density fraction relative to electron density": "ixc =126  *Carbon density fraction relative to electron density \nboundu(126)=0.010D0 \nboundl(126)=1.00D-8", #Iterations
        "nitrogen fraction relative to electron density": "ixc =127  *Nitrogen fraction relative to electron density \nboundu(127)=0.010D0 \nboundl(127)=1.00D-8", #Iterations
        "oxygen density fraction relative to electron density": "ixc =128  *Oxygen density fraction relative to electron density \nboundu(128)=0.010D0 \nboundl(128)=1.00D-8", #Iterations
        "neon density fraction relative to electron density": "ixc =129  *Neon density fraction relative to electron density \nboundu(129)=0.010D0 \nboundl(129)=1.00D-8", #Iterations
        "silicon density fraction relative to electron density": "ixc =130  *Silicon density fraction relative to electron density \nboundu(130)=0.010D0 \nboundl(130)=1.00D-8", #Iterations
        "argon density fraction relative to electron density": "ixc =131  *Argon density fraction relative to electron density \nboundu(131)=0.010D0 \nboundl(131)=1.00D-8", #Iterations
        "iron density fraction relative to electron density": "ixc =132  *Iron density fraction relative to electron density \nboundu(132)=0.010D0 \nboundl(132)=1.00D-8", #Iterations
        "nickel density fraction relative to electron density": "ixc =133  *Nickel density fraction relative to electron density \nboundu(133)=0.010D0 \nboundl(133)=1.00D-8", #Iterations
        "krypton density fraction relative to electron density": "ixc =134  *Krypton density fraction relative to electron density \nboundu(134)=0.010D0 \nboundl(134)=1.00D-8", #Iterations
        "xenon density fraction relative to electron density": "ixc =135  *Xenon density fraction relative to electron density \nboundu(135)=0.010D0 \nboundl(135)=1.00D-8", #Iterations
        "tungsten density fraction relative to electron density": "ixc =136  *Tungsten density fraction relative to electron density \nboundu(136)=0.010D0 \nboundl(136)=1.00D-8", #Iterations
        "fplhsep (f-value for equation 73)": "ixc =137  *fplhsep (f-value for equation 73) \nboundu(137)=1.000D0 \nboundl(137)=0.001D0", #Iterations
        "rebco_thickness : thickness of REBCO layer in tape (m)": "ixc =138  *rebco_thickness : thickness of REBCO layer in tape (m) \nboundu(138)=100.0D-6 \nboundl(138)=0.01D-6", #Iterations
        "copper_thick : thickness of copper layer in tape (m)": "ixc =139  *copper_thick : thickness of copper layer in tape (m) \nboundu(139)=1.00D-3 \nboundl(139)=1.00D-6", #Iterations
        "dr_tf_wp : radial thickness of TFC winding pack (m)": "ixc =140  *dr_tf_wp : radial thickness of TFC winding pack (m) \nboundu(140)=2.000D0 \nboundl(140)=0.001D0", #Iterations
        "fcqt : TF coil quench temperature < tmax_croco (f-value for equation 74)": "ixc =141  *fcqt : TF coil quench temperature < tmax_croco (f-value for equation 74) \nboundu(141)=1.000D0 \nboundl(141)=0.001D0", #Iterations
        "nesep : electron density at separatrix [m-3]": "ixc =142  *nesep : electron density at separatrix [m-3] \nboundu(142)=1.00D20 \nboundl(142)=1.00D17", #Iterations
        "f_copperA_m2 : TF coil current / copper area < Maximum value": "ixc =143  *f_copperA_m2 : TF coil current / copper area < Maximum value \nboundu(143)=1.000D0 \nboundl(143)=0.001D0", #Iterations
        "fnesep : Eich critical electron density at separatrix": "ixc =144  *fnesep : Eich critical electron density at separatrix \nboundu(144)=1.000D0 \nboundl(144)=0.001D0", #Iterations
        "fcpttf fraction of Greenwald density to set as pedestal-top density": "ixc = 145 *fcpttf fraction of Greenwald density to set as pedestal-top density \nboundu(145)=1.000D0 \nboundl(145)=0.500D0", #Iterations
        "fcpttf : F-value for TF coil current per turn limit (constraint equation 77)": "ixc =146  *fcpttf : F-value for TF coil current per turn limit (constraint equation 77) \nboundu(146)=1.000D0 \nboundl(146)=0.001D0", #Iterations
        "freinke : F-value for Reinke detachment criterion (constraint equation 78)": "ixc =147  *freinke : F-value for Reinke detachment criterion (constraint equation 78) \nboundu()=1.000D0 \nboundl(147)=0.001D0", #Iterations
        "fzactual : fraction of impurity at SOL with Reinke detachment criterion": "ixc =148  *fzactual : fraction of impurity at SOL with Reinke detachment criterion \nboundu(148)=1.000D0 \nboundl(148)=1.00D-8", #Iterations
        "fbmaxcs : F-value for max peak CS field (con. 79, itvar 149)": "ixc =  *fbmaxcs : F-value for max peak CS field (con. 79, itvar 149) \nboundu(149)=1.000D0 \nboundl(149)=0.001D0", #Iterations
        "fbmaxcs : Ratio of separatrix density to Greenwald density": "ixc =152  *fbmaxcs : Ratio of separatrix density to Greenwald density \nboundu(152)=1.000D0 \nboundl(152)=0.001D0", #Iterations
        "fpdivlim : F-value for minimum pdivt (con. 80)": "ixc =153  *fpdivlim : F-value for minimum pdivt (con. 80) \nboundu(153)=1.000D0 \nboundl(153)=0.001D0", #Iterations
        "fne0 : F-value for ne(0) > ne(ped) (con. 81)": "ixc =154  *fne0 : F-value for ne(0) > ne(ped) (con. 81) \nboundu(154)=1.000D0 \nboundl(154)=0.001D0", #Iterations
        "pfusife : IFE input fusion power (MW) (ifedrv=3 only)": "ixc =155  *pfusife : IFE input fusion power (MW) (ifedrv=3 only) \nboundu(155)=3.000d3 \nboundl(155)=5.000d2", #Iterations
        "rrin : Input IFE repetition rate (Hz) (ifedrv=3 only)": "ixc =156  *rrin : Input IFE repetition rate (Hz) (ifedrv=3 only) \nboundu(156)=1.000d1 \nboundl(156)=1.000d0", #Iterations
        "fvssu : F-value for available to required start up flux (con. 51)": "ixc =157  *fvssu : F-value for available to required start up flux (con. 51) \nboundu(157)=1.000d1 \nboundl(157)=1.00d-3", #Iterations
        "croco_thick : Thickness of CroCo copper tube (m)": "ixc =158  *croco_thick : Thickness of CroCo copper tube (m) \nboundu(158)=1.0d-1 \nboundl(158)=1.0d-3", #Iterations
        "ftoroidalgap : F-value for toroidalgap >  tftort constraint (con. 82)": "ixc =159  *ftoroidalgap : F-value for toroidalgap >  tftort constraint (con. 82) \nboundu(159)=1.0D0 \nboundl(159)=1.0D-4", #Iterations
        "f_avspace (f-value for equation 83)": "ixc =160  *f_avspace (f-value for equation 83) \nboundu(160)=1.000D0 \nboundl(160)=0.010D0", #Iterations
        "fbetatry_lower (f-value for equation 84)": "ixc =161  *fbetatry_lower (f-value for equation 84) \nboundu(161)=1.000D0 \nboundl(161)=0.010D0", #Iterations
        "r_cp_top : Top outer radius of the centropost (ST only) (m)": "ixc =162  *r_cp_top : Top outer radius of the centropost (ST only) (m) \nboundu(162)=10.000D0 \nboundl(162)=0.0010D0", #Iterations
        "f_t_turn_tf : Top outer radius of the centropost (ST only) (m)": "ixc =163  *f_t_turn_tf : Top outer radius of the centropost (ST only) (m) \nboundu(163)=1000.0D0 \nboundl(163)=0.0010D0", #Iterations
        "f-value for maximum cryogenic plant power": "ixc =164  *f-value for maximum cryogenic plant power \nboundu(164)=1.000D0 \nboundl(164)=0.001D0", #Iterations
        "f-value for maximum TF coil strain": "ixc =165  *f-value for maximum TF coil strain \nboundu(165)=1.0d0 \nboundl(165)=1.0d-9", #Iterations
        "f_copperaoh_m2 : CS coil current / copper area < Maximum value": "ixc =166  * \nboundu(166)=1.000D0 \nboundl(166)=0.001D0", #Iterations
        "fncycle : f-value for minimum CS coil stress load cycles": "ixc =167  *fncycle : f-value for minimum CS coil stress load cycles \nboundu(167)=1.0d0 \nboundl(167)=1.0d-8", #Iterations
        "fecrh_ignition (f-value for equation 91)": "ixc =168  *fecrh_ignition (f-value for equation 91) \nboundu(168)=2.000D0 \nboundl(168)=0.010D0", #Iterations
        "te0_ecrh_achievable (iteration parameter for equation 91)": "ixc =169  *te0_ecrh_achievable (iteration parameter for equation 91) \nboundu(169)=1.0d3 \nboundl(169)=1.0d0", #Iterations
        "beta_div : field line angle wrt divertor target plate (degrees)": "ixc =170  *beta_div : field line angle wrt divertor target plate (degrees) \nboundu(170)=5.01 \nboundl(170)=0.49", #Iterations
        
    }
    create_checkboxes("Select Iterations", Iteration_values, 'Iteration')

#Scane Module For 1 Dimention
def on_select_1d():
    nsweep_values = [
     "1 *aspect", "2 *hldivlim", "3 *pnetelin", "4 *hfact", "5 *oacdcp",
     "6 *walalw", "7 *beamfus0", "8 *fqval", "9 *te", "10 *boundu(15: fvs)",
     "11 *dnbeta", "12 *bscfmax (use negative values only)", "13 *boundu(10: hfact)",
     "14 *fiooic", "15 *fjprot", "16 *rmajor", "17 *bmxlim", "18 *gammax",
     "19 *boundl(16: ohcth)", "20 *tbrnmn", "21 *not used", "22 *cfactr (N.B. requires iavail=0)",
     "23 *boundu(72: fipir)", "24 *powfmax", "25 *kappa", "26 *triang", 
     "27 *tbrmin (for blktmodel > 0 only)", "28 *bt", "29 *coreradius", 
     "30 *fimpvar # OBSOLETE", "31 *taulimit", "32 *epsvmc", "33 *ttarget", 
     "34 *qtargettotal", "35 *lambda_q_omp", "36 *lambda_target", "37 *lcon_factor", 
     "38 *Neon upper limit", "39 *Argon upper limit", "40 *Xenon upper limit", 
     "41 *blnkoth", "42 *Argon fraction fimp(9)", "43 *normalised minor radius at which electron cyclotron current drive is maximum",
     "44 *Allowable maximum shear stress (Tresca) in tf coil structural material", 
     "45 *Minimum allowable temperature margin ; tf *coils", "46 *boundu(150) fgwsep",
     "47 *impurity_enrichment(9) Argon impurity enrichment", "48 *TF coil - n_pancake (integer turn winding pack)",
     "49 *TF coil - n_layer (integer turn winding pack)", "50 *Xenon fraction fimp(13)",
     "51 *Power fraction to lower DN Divertor ftar", "52 *SoL radiation fraction",
     "54 *GL_nbti upper critical field at 0 Kelvin", "55 *shldith : Inboard neutron shield thickness",
     "56 *crypmw_max: Maximum cryogenic power (ixx=164, ixc=87)", "57 *bt lower boundary",
     "58 *scrapli : Inboard plasma-first wall gap", "59 *scraplo : Outboard plasma-first wall gap",
     "60 *sig_tf_wp_max: Allowable stress in TF Coil conduit (Tresca)", "61 *copperaoh_m2_max : CS coil current / copper area",
     "62 *coheof : CS coil current density at EOF", "63 *ohcth : CS thickness (m)", 
     "64 *ohhghf : CS height (m)", "65 *n_cycle_min : Minimum cycles for CS stress model constraint 90",
     "66 *oh_steel_frac: Steel fraction in CS coil", "67 *t_crack_vertical: Initial crack vertical dimension (m)"
    ]


    dialog = tk.Toplevel(root)
    dialog.title("1D Data Entry")

    tk.Label(dialog, text="Select ist degree nsweep value:").pack(pady=5)
    nsweep_combobox = ttk.Combobox(dialog, values=nsweep_values, state="readonly")
    nsweep_combobox.pack(pady=5)

    tk.Label(dialog, text="Enter sweep values separated by commas:").pack(pady=5)
    sweep_entry = tk.Entry(dialog)
    sweep_entry.pack(pady=5)

    def submit():
        nsweep = nsweep_combobox.get()
        sweep_values = sweep_entry.get()
        if nsweep and sweep_values:
            sweep_list = sweep_values.split(',')
            isweep = len(sweep_list)
            result_text = f"nsweep = {nsweep}\nsweep = {sweep_values}\nisweep = {isweep}\n"
            text_box.insert(tk.END, result_text)
        dialog.destroy()

    tk.Button(dialog, text="Submit", command=submit).pack(pady=10)

#Scan Module For 2 Dimention
def on_select_2d() :
    nsweep_values = [
     "1 *aspect", "2 *hldivlim", "3 *pnetelin", "4 *hfact", "5 *oacdcp",
     "6 *walalw", "7 *beamfus0", "8 *fqval", "9 *te", "10 *boundu(15: fvs)",
     "11 *dnbeta", "12 *bscfmax (use negative values only)", "13 *boundu(10: hfact)",
     "14 *fiooic", "15 *fjprot", "16 *rmajor", "17 *bmxlim", "18 *gammax",
     "19 *boundl(16: ohcth)", "20 *tbrnmn", "21 *not used", "22 *cfactr (N.B. requires iavail=0)",
     "23 *boundu(72: fipir)", "24 *powfmax", "25 *kappa", "26 *triang", 
     "27 *tbrmin (for blktmodel > 0 only)", "28 *bt", "29 *coreradius", 
     "30 *fimpvar # OBSOLETE", "31 *taulimit", "32 *epsvmc", "33 *ttarget", 
     "34 *qtargettotal", "35 *lambda_q_omp", "36 *lambda_target", "37 *lcon_factor", 
     "38 *Neon upper limit", "39 *Argon upper limit", "40 *Xenon upper limit", 
     "41 *blnkoth", "42 *Argon fraction fimp(9)", "43 *normalised minor radius at which electron cyclotron current drive is maximum",
     "44 *Allowable maximum shear stress (Tresca) in tf coil structural material", 
     "45 *Minimum allowable temperature margin ; tf *coils", "46 *boundu(150) fgwsep",
     "47 *impurity_enrichment(9) Argon impurity enrichment", "48 *TF coil - n_pancake (integer turn winding pack)",
     "49 *TF coil - n_layer (integer turn winding pack)", "50 *Xenon fraction fimp(13)",
     "51 *Power fraction to lower DN Divertor ftar", "52 *SoL radiation fraction",
     "54 *GL_nbti upper critical field at 0 Kelvin", "55 *shldith : Inboard neutron shield thickness",
     "56 *crypmw_max: Maximum cryogenic power (ixx=164, ixc=87)", "57 *bt lower boundary",
     "58 *scrapli : Inboard plasma-first wall gap", "59 *scraplo : Outboard plasma-first wall gap",
     "60 *sig_tf_wp_max: Allowable stress in TF Coil conduit (Tresca)", "61 *copperaoh_m2_max : CS coil current / copper area",
     "62 *coheof : CS coil current density at EOF", "63 *ohcth : CS thickness (m)", 
     "64 *ohhghf : CS height (m)", "65 *n_cycle_min : Minimum cycles for CS stress model constraint 90",
     "66 *oh_steel_frac: Steel fraction in CS coil", "67 *t_crack_vertical: Initial crack vertical dimension (m)"
    ]

    nsweep_2_values = [
     "1 *aspect", "2 *hldivlim", "3 *pnetelin", "4 *hfact", "5 *oacdcp",
     "6 *walalw", "7 *beamfus0", "8 *fqval", "9 *te", "10 *boundu(15: fvs)",
     "11 *dnbeta", "12 *bscfmax (use negative values only)", "13 *boundu(10: hfact)",
     "14 *fiooic", "15 *fjprot", "16 *rmajor", "17 *bmxlim", "18 *gammax",
     "19 *boundl(16: ohcth)", "20 *tbrnmn", "21 *not used", "22 *cfactr (N.B. requires iavail=0)",
     "23 *boundu(72: fipir)", "24 *powfmax", "25 *kappa", "26 *triang", 
     "27 *tbrmin (for blktmodel > 0 only)", "28 *bt", "29 *coreradius", 
     "30 *fimpvar # OBSOLETE", "31 *taulimit", "32 *epsvmc", "33 *ttarget", 
     "34 *qtargettotal", "35 *lambda_q_omp", "36 *lambda_target", "37 *lcon_factor", 
     "38 *Neon upper limit", "39 *Argon upper limit", "40 *Xenon upper limit", 
     "41 *blnkoth", "42 *Argon fraction fimp(9)", "43 *normalised minor radius at which electron cyclotron current drive is maximum",
     "44 *Allowable maximum shear stress (Tresca) in tf coil structural material", 
     "45 *Minimum allowable temperature margin ; tf *coils", "46 *boundu(150) fgwsep",
     "47 *impurity_enrichment(9) Argon impurity enrichment", "48 *TF coil - n_pancake (integer turn winding pack)",
     "49 *TF coil - n_layer (integer turn winding pack)", "50 *Xenon fraction fimp(13)",
     "51 *Power fraction to lower DN Divertor ftar", "52 *SoL radiation fraction",
     "54 *GL_nbti upper critical field at 0 Kelvin", "55 *shldith : Inboard neutron shield thickness",
     "56 *crypmw_max: Maximum cryogenic power (ixx=164, ixc=87)", "57 *bt lower boundary",
     "58 *scrapli : Inboard plasma-first wall gap", "59 *scraplo : Outboard plasma-first wall gap",
     "60 *sig_tf_wp_max: Allowable stress in TF Coil conduit (Tresca)", "61 *copperaoh_m2_max : CS coil current / copper area",
     "62 *coheof : CS coil current density at EOF", "63 *ohcth : CS thickness (m)", 
     "64 *ohhghf : CS height (m)", "65 *n_cycle_min : Minimum cycles for CS stress model constraint 90",
     "66 *oh_steel_frac: Steel fraction in CS coil", "67 *t_crack_vertical: Initial crack vertical dimension (m)"
    ]

    dialog = tk.Toplevel(root)
    dialog.title("2D Data Entry")

    tk.Label(dialog, text="Select 1st nsweep value:").pack(pady=5)
    nsweep_combobox = ttk.Combobox(dialog, values=nsweep_values, state="readonly")
    nsweep_combobox.pack(pady=5)

    tk.Label(dialog, text="Enter 1st sweep values separated by commas:").pack(pady=5)
    sweep_entry = tk.Entry(dialog)
    sweep_entry.pack(pady=5)

    tk.Label(dialog, text="Select 2nd nsweep_2 value:").pack(pady=5)
    nsweep_2_combobox = ttk.Combobox(dialog, values=nsweep_2_values, state="readonly")
    nsweep_2_combobox.pack(pady=5)

    tk.Label(dialog, text="Enter 2nd sweep_2 values separated by commas:").pack(pady=5)
    sweep_2_entry = tk.Entry(dialog)
    sweep_2_entry.pack(pady=5)

    def submit():
        nsweep = nsweep_combobox.get()
        sweep_values = sweep_entry.get()
        nsweep_2 = nsweep_2_combobox.get()
        sweep_2_values = sweep_2_entry.get()
        if nsweep and sweep_values and nsweep_2 and sweep_2_values :
            sweep_list = sweep_values.split(',')
            isweep = len(sweep_list)
            sweep_2_list = sweep_2_values.split(',')
            isweep_2 = len(sweep_2_list)
            result_text = f"nsweep = {nsweep}\nsweep = {sweep_values}\nisweep = {isweep}\nnsweep_2 = {nsweep_2}\nsweep_2 = {sweep_2_values}\nisweep_2 = {isweep_2}\n"
            text_box.insert(tk.END, result_text)
        dialog.destroy()

    tk.Button(dialog, text="Submit", command=submit).pack(pady=10)

def Scan_Module(event):
    submenu.post(event.x_root, event.y_root)


#Build Variables Encapsule
def Build():
    Build_values = {
        "Minimum minor radius (m)":"aplasmin=0.25         *minimum minor radius (m)",  #BUILD
         "Inboard blanket box manifold thickness (m) (blktmodel>0)":"blbmith=0.17         *inboard blanket box manifold thickness (m) (blktmodel>0)",  #BUILD
         "Outboard blanket box manifold thickness (m) (blktmodel>0)":"blbmoth=0.27         *outboard blanket box manifold thickness (m) (blktmodel>0)",  #BUILD
         "Inboard blanket base plate thickness (m) (blktmodel>0)":"blbpith=0.3         *inboard blanket base plate thickness (m) (blktmodel>0)",  #BUILD
         "Outboard blanket base plate thickness (m) (blktmodel>0)":"blbpoth=0.35         *outboard blanket base plate thickness (m) (blktmodel>0)",  #BUILD
         "Inboard blanket breeding zone thickness (m) (blktmodel>0) (iteration variable 90)":"blbuith=0.365         *inboard blanket breeding zone thickness (m) (blktmodel>0) (iteration variable 90)",  #BUILD
         "Outboard blanket breeding zone thickness (m) (blktmodel>0) (iteration variable 91)":"blbuoth=0.465         *outboard blanket breeding zone thickness (m) (blktmodel>0) (iteration variable 91)",  #BUILD
         "Inboard blanket thickness (m); (calculated if blktmodel>0) (=0.0 if iblnkith=0)":"blnkith=0.115         *inboard blanket thickness (m); (calculated if blktmodel>0) (=0.0 if iblnkith=0)",  #BUILD
         "Outboard blanket thickness (m); calculated if blktmodel>0":"blnkoth=0.235         *outboard blanket thickness (m); calculated if blktmodel>0",  #BUILD
         "Top blanket thickness (m), = mean of inboard and outboard blanket thicknesses":"blnktth=-         *top blanket thickness (m), = mean of inboard and outboard blanket thicknesses",  #BUILD
         "Central solenoid inboard radius (m) (iteration variable 29)":"bore=1.42         *central solenoid inboard radius (m) (iteration variable 29)",  #BUILD
         "Cryostat lid height scaling factor (tokamaks)":"clhsf=4.268         *cryostat lid height scaling factor (tokamaks)",  #BUILD
         "Cryostat thickness (m)":"ddwex=0.07         *cryostat thickness (m)",  #BUILD
         "Vacuum vessel inboard thickness (TF coil / shield) (m)":"d_vv_in=0.07         *vacuum vessel inboard thickness (TF coil / shield) (m)",  #BUILD
         "Vacuum vessel outboard thickness (TF coil / shield) (m)":"d_vv_out=0.07         *vacuum vessel outboard thickness (TF coil / shield) (m)",  #BUILD
         "Vacuum vessel topside thickness (TF coil / shield) (m) (= d_vv_bot if double-null)":"d_vv_top=0.07         *vacuum vessel topside thickness (TF coil / shield) (m) (= d_vv_bot if double-null)",  #BUILD
         "Vacuum vessel underside thickness (TF coil / shield) (m)":"d_vv_bot=0.07         *vacuum vessel underside thickness (TF coil / shield) (m)",  #BUILD
         "F-value for stellarator radial space check (constraint equation 83)":"f_avspace=1         *F-value for stellarator radial space check (constraint equation 83)",  #BUILD
         "Fraction of space occupied by CS pre-compression structure":"fcspc=0.6         *Fraction of space occupied by CS pre-compression structure",  #BUILD
         "Separation force in CS coil pre-compression structure":"fseppc=350000000         *Separation force in CS coil pre-compression structure",  #BUILD
         "Gap between inboard vacuum vessel and thermal shield (m) (iteration variable 61)":"gapds=0.155         *gap between inboard vacuum vessel and thermal shield (m) (iteration variable 61)",  #BUILD
         "Gap between central solenoid and TF coil (m) (iteration variable 42)":"gapoh=0.08         *gap between central solenoid and TF coil (m) (iteration variable 42)",  #BUILD
         "Minimum gap between outboard vacuum vessel and TF coil (m) (iteration variable 31)":"gapomin=0.234         *minimum gap between outboard vacuum vessel and TF coil (m) (iteration variable 31)",  #BUILD
         "Switch for existence of central solenoid:":"iohcl=1         *Switch for existence of central solenoid:",  #BUID
         "Switch for existence of central solenoid pre-compression structure:":"iprecomp=1         *Switch for existence of central solenoid pre-compression structure:",  #BUID
         "Central solenoid thickness (m) (iteration variable 16)":"ohcth=0.811         *Central solenoid thickness (m) (iteration variable 16)",  #BUID
         "Plasma inboard radius (m) (consistency equation 29)":"rinboard=0.651         *plasma inboard radius (m) (consistency equation 29)",  #BUID
         "Ratio between the top and the midplane TF CP outer radius [-] Not used by default (-1) must be larger than 1 otherwise":"f_r_cp=1.4         *Ratio between the top and the midplane TF CP outer radius [-] Not used by default (-1) must be larger than 1 otherwise",  #BUID
         "Gap between plasma and first wall, inboard side (m) (if iscrp=1) Iteration variable: ixc = 73 Scan variable: nsweep = 58":"scrapli=0.14         *Gap between plasma and first wall, inboard side (m) (if iscrp=1) Iteration variable: ixc = 73 Scan variable: nsweep = 58",  #BUID
         "Gap between plasma and first wall, outboard side (m) (if iscrp=1) Iteration variable: ixc = 74 Scan variable: nsweep = 59":"scraplo=0.15         *Gap between plasma and first wall, outboard side (m) (if iscrp=1) Iteration variable: ixc = 74 Scan variable: nsweep = 59",  #BUID
         "Inboard shield thickness (m) (iteration variable 93)":"shldith=0.69         *inboard shield thickness (m) (iteration variable 93)",  #BUID
         "Lower (under divertor) shield thickness (m)":"shldlth=0.7         *lower (under divertor) shield thickness (m)",  #BUID
         "Outboard shield thickness (m) (iteration variable 94)":"shldoth=1.05         *outboard shield thickness (m) (iteration variable 94)",  #BUID
         "Upper/lower shield thickness (m); calculated if blktmodel > 0 (= shldlth if double-null)":"shldtth=0.6         *upper/lower shield thickness (m); calculated if blktmodel > 0 (= shldlth if double-null)",  #BUID
         "Allowable stress in CSpre-compression structure (Pa)":"sigallpc=300000000         *allowable stress in CSpre-compression structure (Pa)",  #BUID
         "TF coil outboard leg / inboard leg radial thickness ratio (i_tf_sup=0 only) (iteration variable 75)":"tfootfi=1.19         *TF coil outboard leg / inboard leg radial thickness ratio (i_tf_sup=0 only) (iteration variable 75)",  #BUID
         "Minimum metal-to-metal gap between TF coil and thermal shield (m)":"tftsgap=0.05         *Minimum metal-to-metal gap between TF coil and thermal shield (m)",  #BUID
         "TF-VV thermal shield thickness, inboard (m)":"thshield_ib=0.05         *TF-VV thermal shield thickness, inboard (m)",  #BUID
         "TF-VV thermal shield thickness, outboard (m)":"thshield_ob=0.05         *TF-VV thermal shield thickness, outboard (m)",  #BUID
         "TF-VV thermal shield thickness, vertical build (m)":"thshield_vb=0.05         *TF-VV thermal shield thickness, vertical build (m)",  #BUID
         "Vertical gap between vacuum vessel and thermal shields (m)":"vgap2=0.163         *vertical gap between vacuum vessel and thermal shields (m)",  #BUID
         "Vertical gap between top of plasma and first wall (m) (= vgap if double-null)":"vgaptop=0.6         *vertical gap between top of plasma and first wall (m) (= vgap if double-null)",  #BUID
         "Gap between vacuum vessel and blanket (m)":"vvblgap=0.05         *gap between vacuum vessel and blanket (m)",  #BUID
         "Length of inboard divertor plate (m)":"plleni=1         *length of inboard divertor plate (m)",  #BUID
         "Length of outboard divertor plate (m)":"plleno=1         *length of outboard divertor plate (m)",  #BUID
         "Poloidal length, x-point to inboard strike point (m)":"plsepi=1         *poloidal length, x-point to inboard strike point (m)",  #BUID
         "Poloidal length, x-point to outboard strike point (m)":"plsepo=1.5         *poloidal length, x-point to outboard strike point (m)",  #BUID

    }
    create_checkboxes("Select Build Variable", Build_values, 'Build')

#Constraint Variables Encapsule
def Constraint_variables():
    """Display a list of checkboxes for the user to select Constraint Variables, with a scrollbar."""
    Constraint_variables_values = {
         "Minimum auxiliary power (MW) (constraint equation 40)":"auxmin=0.1     *minimum auxiliary power (MW) (constraint equation 40)", #Constraint variables
         "Maximum poloidal beta (constraint equation 48)":"betpmx=0.19     *maximum poloidal beta (constraint equation 48)", #Constraint variables
         "Minimum fusion gain Q (constraint equation 28)":"bigqmin=10     *minimum fusion gain Q (constraint equation 28)", #Constraint variables
         "Maximum peak toroidal field (T) (constraint equation 25)":"bmxlim=12     *maximum peak toroidal field (T) (constraint equation 25)", #Constraint variables
         "F-value for minimum auxiliary power (constraint equation 40, iteration variable 64)":"fauxmn=1     *f-value for minimum auxiliary power (constraint equation 40, iteration variable 64)", #Constraint variables
         "F-value for epsilon beta-poloidal (constraint equation 6, iteration variable 8)":"fbeta=1     *f-value for epsilon beta-poloidal (constraint equation 6, iteration variable 8)", #Constraint variables
         "F-value for poloidal beta (constraint equation 48, iteration variable 79)":"fbetap=1     *f-value for poloidal beta (constraint equation 48, iteration variable 79)", #Constraint variables
         "F-value for beta limit (constraint equation 24, iteration variable 36)":"fbetatry=1     *f-value for beta limit (constraint equation 24, iteration variable 36)", #Constraint variables
         "F-value for (lower) beta limit (constraint equation 84, iteration variable 173)":"fbetatry_lower=1     *f-value for (lower) beta limit (constraint equation 84, iteration variable 173)", #Constraint variables
         "F-value for TF coil current per turn upper limit (constraint equation 77, iteration variable 146)":"fcpttf=1     *f-value for TF coil current per turn upper limit (constraint equation 77, iteration variable 146)", #Constraint variables
         "F-value for conducting wall radius / rminor limit (constraint equation 23, iteration variable 104)":"fcwr=1     *f-value for conducting wall radius / rminor limit (constraint equation 23, iteration variable 104)", #Constraint variables
         "F-value for density limit (constraint equation 5, iteration variable 9) (invalid if ipedestal=3)":"fdene=1     *f-value for density limit (constraint equation 5, iteration variable 9) (invalid if ipedestal=3)", #Constraint variables
         "F-value for divertor collisionality (constraint equation 22, iteration variable 34)":"fdivcol=1     *f-value for divertor collisionality (constraint equation 22, iteration variable 34)", #Constraint variables
         "F-value for first wall coolant temperature rise (constraint equation 38, iteration variable 62)":"fdtmp=1     *f-value for first wall coolant temperature rise (constraint equation 38, iteration variable 62)", #Constraint variables
         "F-value for ecrh ignition constraint (constraint equation 91, iteration variable 168)":"fecrh_ignition=1     *f-value for ecrh ignition constraint (constraint equation 91, iteration variable 168)", #Constraint variables
         "F-value for neutron fluence on TF coil (constraint equation 53, iteration variable 92)":"fflutf=1     *f-value for neutron fluence on TF coil (constraint equation 53, iteration variable 92)", #Constraint variables
         "F-value for maximum fusion power (constraint equation 9, iteration variable 26)":"ffuspow=1     *f-value for maximum fusion power (constraint equation 9, iteration variable 26)", #Constraint variables
         "F-value for current drive gamma (constraint equation 37, iteration variable 40)":"fgamcd=1     *f-value for current drive gamma (constraint equation 37, iteration variable 40)", #Constraint variables
         "F-value for divertor heat load (constraint equation 18, iteration variable 27)":"fhldiv=1     *f-value for divertor heat load (constraint equation 18, iteration variable 27)", #Constraint variables
         "F-value for TF coil operating current / critical current ratio (constraint equation 33, iteration variable 50)":"fiooic=0.5     *f-value for TF coil operating current / critical current ratio (constraint equation 33, iteration variable 50)", #Constraint variables
         "F-value for Ip/Irod upper limit constraint equation icc = 46 iteration variable ixc = 72":"fipir=1     *f-value for Ip/Irod upper limit constraint equation icc = 46 iteration variable ixc = 72", #Constraint variables
         "F-value for central solenoid current at end-of-flattop (constraint equation 26, iteration variable 38)":"fjohc=1     *f-value for central solenoid current at end-of-flattop (constraint equation 26, iteration variable 38)", #Constraint variables
         "F-value for central solenoid current at beginning of pulse (constraint equation 27, iteration variable 39)":"fjohc0=1     *f-value for central solenoid current at beginning of pulse (constraint equation 27, iteration variable 39)", #Constraint variables
         "F-value for TF coil winding pack current density (constraint equation 35, iteration variable 53)":"fjprot=1     *f-value for TF coil winding pack current density (constraint equation 35, iteration variable 53)", #Constraint variables
         "F-value for L-H power threshold (constraint equation 15, iteration variable 103)":"flhthresh=1     *f-value for L-H power threshold (constraint equation 15, iteration variable 103)", #Constraint variables
         "F-value for maximum MVA (constraint equation 19, iteration variable 30)":"fmva=1     *f-value for maximum MVA (constraint equation 19, iteration variable 30)", #Constraint variables
         "F-value for maximum neutral beam shine-through fraction (constraint equation 59, iteration variable 105)":"fnbshinef=1     *f-value for maximum neutral beam shine-through fraction (constraint equation 59, iteration variable 105)", #Constraint variables
         "F-value for minimum CS coil stress load cycles (constraint equation 90, iteration variable 167)":"fncycle=1     *f-value for minimum CS coil stress load cycles (constraint equation 90, iteration variable 167)", #Constraint variables
         "F-value for Eich critical separatrix density (constraint equation 76, iteration variable 144)":"fnesep=1     *f-value for Eich critical separatrix density (constraint equation 76, iteration variable 144)", #Constraint variables
         "F-value for Tresca yield criterion in Central Solenoid (constraint equation 72, iteration variable 123)":"foh_stress=1     *f-value for Tresca yield criterion in Central Solenoid (constraint equation 72, iteration variable 123)", #Constraint variables
         "F-value for maximum toroidal field (constraint equation 25, iteration variable 35)":"fpeakb=1     *f-value for maximum toroidal field (constraint equation 25, iteration variable 35)", #Constraint variables
         "F-value for injection power (constraint equation 30, iteration variable 46)":"fpinj=1     *f-value for injection power (constraint equation 30, iteration variable 46)", #Constraint variables
         "F-value for net electric power (constraint equation 16, iteration variable 25)":"fpnetel=1     *f-value for net electric power (constraint equation 16, iteration variable 25)", #Constraint variables
         "F-value for neutral beam tangency radius limit (constraint equation 20, iteration variable 33)":"fportsz=1     *f-value for neutral beam tangency radius limit (constraint equation 20, iteration variable 33)", #Constraint variables
         "F-value for maximum Psep*Bt/qAR limit (constraint equation 68, iteration variable 117)":"fpsepbqar=1     *f-value for maximum Psep*Bt/qAR limit (constraint equation 68, iteration variable 117)", #Constraint variables
         "F-value for maximum Psep/R limit (constraint equation 56, iteration variable 97)":"fpsepr=1     *f-value for maximum Psep/R limit (constraint equation 56, iteration variable 97)", #Constraint variables
         "F-value for peak centrepost temperature (constraint equation 44, iteration variable 68)":"fptemp=1     *f-value for peak centrepost temperature (constraint equation 44, iteration variable 68)", #Constraint variables
         "F-value for maximum TF coil nuclear heating (constraint equation 54, iteration variable 95)":"fptfnuc=1     *f-value for maximum TF coil nuclear heating (constraint equation 54, iteration variable 95)", #Constraint variables
         "F-value for edge safety factor (constraint equation 45, iteration variable 71)":"fq=1     *f-value for edge safety factor (constraint equation 45, iteration variable 71)", #Constraint variables
         "F-value for Q (constraint equation 28, iteration variable 45)":"fqval=1     *f-value for Q (constraint equation 28, iteration variable 45)", #Constraint variables
         "F-value for core radiation power limit (constraint equation 17, iteration variable 28)":"fradpwr=0.99     *f-value for core radiation power limit (constraint equation 17, iteration variable 28)", #Constraint variables
         "F-value for upper limit on radiation wall load (constr. equ. 67, iteration variable 116)":"fradwall=1     *f-value for upper limit on radiation wall load (constr. equ. 67, iteration variable 116)", #Constraint variables
         "F-value for Reinke detachment criterion (constr. equ. 78, iteration variable 147)":"freinke=1     *f-value for Reinke detachment criterion (constr. equ. 78, iteration variable 147)", #Constraint variables
         "F-value for minor radius limit (constraint equation 21, iteration variable 32)":"frminor=1     *f-value for minor radius limit (constraint equation 21, iteration variable 32)", #Constraint variables
         "F-value for maximum TF coil case Tresca yield criterion (constraint equation 31, iteration variable 48)":"fstrcase=1     *f-value for maximum TF coil case Tresca yield criterion (constraint equation 31, iteration variable 48)", #Constraint variables
         "F-value for maxiumum TF coil conduit Tresca yield criterion (constraint equation 32, iteration variable 49)":"fstrcond=1     *f-value for maxiumum TF coil conduit Tresca yield criterion (constraint equation 32, iteration variable 49)", #Constraint variables
         "F-value for maxiumum TF coil strain absolute value (constraint equation 88, iteration variable 165)":"fstr_wp=1     *f-value for maxiumum TF coil strain absolute value (constraint equation 88, iteration variable 165)", #Constraint variables
         "F-value for maximum permitted stress of the VV (constraint equation 65, iteration variable 113)":"fmaxvvstress=1     *f-value for maximum permitted stress of the VV (constraint equation 65, iteration variable 113)", #Constraint variables
         "F-value for minimum tritium breeding ratio (constraint equation 52, iteration variable 89)":"ftbr=1     *f-value for minimum tritium breeding ratio (constraint equation 52, iteration variable 89)", #Constraint variables
         "F-value for minimum burn time (constraint equation 13, iteration variable 21)":"ftburn=1     *f-value for minimum burn time (constraint equation 13, iteration variable 21)", #Constraint variables
         "F-value for cycle time (constraint equation 42, iteration variable 67)":"ftcycl=1     *f-value for cycle time (constraint equation 42, iteration variable 67)", #Constraint variables
         "F-value for central solenoid temperature margin (constraint equation 60, iteration variable 106)":"ftmargoh=1     *f-value for central solenoid temperature margin (constraint equation 60, iteration variable 106)", #Constraint variables
         "F-value for TF coil temperature margin (constraint equation 36, iteration variable 54)":"ftmargtf=1     *f-value for TF coil temperature margin (constraint equation 36, iteration variable 54)", #Constraint variables
         "F-value for plasma current ramp-up time (constraint equation 41, iteration variable 66)":"ftohs=1     *f-value for plasma current ramp-up time (constraint equation 41, iteration variable 66)", #Constraint variables
         "F-value for first wall peak temperature (constraint equation 39, iteration variable 63)":"ftpeak=1     *f-value for first wall peak temperature (constraint equation 39, iteration variable 63)", #Constraint variables
         "F-value for dump voltage (constraint equation 34, iteration variable 51)":"fvdump=1     *f-value for dump voltage (constraint equation 34, iteration variable 51)", #Constraint variables
         "F-value for flux-swing (V-s) requirement (STEADY STATE) (constraint equation 12, iteration variable 15)":"fvs=1     *f-value for flux-swing (V-s) requirement (STEADY STATE) (constraint equation 12, iteration variable 15)", #Constraint variables
         "F-value for vacuum vessel He concentration limit (iblanket = 2) (constraint equation 55, iteration variable 96)":"fvvhe=1     *f-value for vacuum vessel He concentration limit (iblanket = 2) (constraint equation 55, iteration variable 96)", #Constraint variables
         "F-value for maximum wall load (constraint equation 8, iteration variable 14)":"fwalld=1     *f-value for maximum wall load (constraint equation 8, iteration variable 14)", #Constraint variables
         "F-value for maximum zeff (constraint equation 64, iteration variable 112)":"fzeffmax=1     *f-value for maximum zeff (constraint equation 64, iteration variable 112)", #Constraint variables
         "Maximum current drive gamma (constraint equation 37)":"gammax=2     *maximum current drive gamma (constraint equation 37)", #Constraint variables
         "Maximum permitted radiation wall load (MW/m^2) (constraint equation 67)":"maxradwallload=1     *Maximum permitted radiation wall load (MW/m^2) (constraint equation 67)", #Constraint variables
         "Maximum MVA limit (constraint equation 19)":"mvalim=40     *maximum MVA limit (constraint equation 19)", #Constraint variables
         "Maximum neutral beam shine-through fraction (constraint equation 59)":"nbshinefmax=0.001     *maximum neutral beam shine-through fraction (constraint equation 59)", #Constraint variables
         "Max fast neutron fluence on TF coil (n/m2) (blktmodel>0) ":"nflutfmax=1.00E+23     *max fast neutron fluence on TF coil (n/m2) (blktmodel>0)", #Constraint variables
         "Minimum pdivt [MW] (constraint equation 80)":"pdivtlim=150     *Minimum pdivt [MW] (constraint equation 80)", #Constraint variables
         "Peaking factor for radiation wall load (constraint equation 67)":"peakfactrad=3.33     *peaking factor for radiation wall load (constraint equation 67)", #Constraint variables
         "Peak radiation wall load (MW/m^2) (constraint equation 67)":"peakradwallload=-     *Peak radiation wall load (MW/m^2) (constraint equation 67)", #Constraint variables
         "Required net electric power (MW) (constraint equation 16)":"pnetelin=1000     *required net electric power (MW) (constraint equation 16)", #Constraint variables
         "Maximum fusion power (MW) (constraint equation 9)":"powfmax=1500     *maximum fusion power (MW) (constraint equation 9)", #Constraint variables
         "Maximum ratio of Psep*Bt/qAR (MWT/m) (constraint equation 68)":"psepbqarmax=9.5     *maximum ratio of Psep*Bt/qAR (MWT/m) (constraint equation 68)", #Constraint variables
         "Maximum ratio of power crossing the separatrix to plasma major radius (Psep/R) (MW/m) (constraint equation 56)":"pseprmax=25     *maximum ratio of power crossing the separatrix to plasma major radius (Psep/R) (MW/m) (constraint equation 56)", #Constraint variables
         "Maximum nuclear heating in TF coil (MW/m3) (constraint equation 54)":"ptfnucmax=0.001     *maximum nuclear heating in TF coil (MW/m3) (constraint equation 54)", #Constraint variables
         "Minimum tritium breeding ratio (constraint equation 52)":"tbrmin=1.1     *minimum tritium breeding ratio (constraint equation 52)", #Constraint variables
         "Minimum burn time (s) (KE - no longer itv., see issue #706)":"tbrnmn=1     *minimum burn time (s) (KE - no longer itv., see issue #706)", #Constraint variables
         "Minimum cycle time (s) (constraint equation 42)":"tcycmn=-     *minimum cycle time (s) (constraint equation 42)", #Constraint variables
         "Minimum plasma current ramp-up time (s) (constraint equation 41)":"tohsmn=1     *minimum plasma current ramp-up time (s) (constraint equation 41)", #Constraint variables
         "Allowed maximum helium concentration in vacuum vessel at end of plant life (appm) (iblanket =2) (constraint equation 55)":"vvhealw=1     *allowed maximum helium concentration in vacuum vessel at end of plant life (appm) (iblanket =2) (constraint equation 55)", #Constraint variables
         "Allowable neutron wall-load (MW/m2) (constraint equation 8)":"walalw=1     *allowable neutron wall-load (MW/m2) (constraint equation 8)", #Constraint variables
         "Lower limit on taup/taueff the ratio of alpha particle to energy confinement times (constraint equation 62)":"taulimit=5     *Lower limit on taup/taueff the ratio of alpha particle to energy confinement times (constraint equation 62)", #Constraint variables
         "F-value for lower limit on taup/taueff the ratio of alpha particle to energy confinement times (constraint equation 62, iteration variable 110)":"ftaulimit=1     *f-value for lower limit on taup/taueff the ratio of alpha particle to energy confinement times (constraint equation 62, iteration variable 110)", #Constraint variables
         "F-value for constraint that number of pumps < tfno (constraint equation 63, iteration variable 111)":"fniterpump=1     *f-value for constraint that number of pumps < tfno (constraint equation 63, iteration variable 111)", #Constraint variables
         "Maximum value for Zeff (constraint equation 64)":"zeffmax=3.6     *maximum value for Zeff (constraint equation 64)", #Constraint variables
         "F-value for constraint on rate of change of energy in poloidal field (constraint equation 66, iteration variable 115)":"fpoloidalpower=1     *f-value for constraint on rate of change of energy in poloidal field (constraint equation 66, iteration variable 115)", #Constraint variables
         "F-value to ensure separatrix power is less than value from Kallenbach divertor (Not required as constraint 69 is an equality)":"fpsep=1     *f-value to ensure separatrix power is less than value from Kallenbach divertor (Not required as constraint 69 is an equality)", #Constraint variables
         "TF coil quench temparature remains below tmax_croco (constraint equation 74, iteration variable 141)":"fcqt=1     *TF coil quench temparature remains below tmax_croco (constraint equation 74, iteration variable 141)", #Constraint variables

    }
    create_checkboxes("Select Constraint Variables", Constraint_variables_values, 'Constraint_variable')

#Cost Variables Encapsule
def Cost_variables():
    """Display a list of checkboxes for the user to select Cost Variables, with a scrollbar."""
    Cost_variables_values = {
        "Allowable first wall/blanket neutron fluence (MW-yr/m2) (blktmodel=0)":"abktflnc=5     *allowable first wall/blanket neutron fluence (MW-yr/m2) (blktmodel=0)",  #COST
         "Allowable divertor heat fluence (MW-yr/m2)":"adivflnc=7     *allowable divertor heat fluence (MW-yr/m2)",  #COST
         "Fixed cost of superconducting cable ($/m)":"cconfix=80     *fixed cost of superconducting cable ($/m)",  #COST
         "Cost of PF coil steel conduit/sheath ($/m)":"cconshpf=70     *cost of PF coil steel conduit/sheath ($/m)",  #COST
         "Cost of TF coil steel conduit/sheath ($/m)":"cconshtf=75     *cost of TF coil steel conduit/sheath ($/m)",  #COST
         "Total plant availability fraction; input if iavail=0":"cfactr=0.75     *Total plant availability fraction; input if iavail=0",  #COST
         "Indirect cost factor (func of lsa) (cost model = 0)":"cfind=[0.244 0.244 0.244 0.29 ]     *indirect cost factor (func of lsa) (cost model = 0)",  #COST
         "Cost of land (M$)":"cland=19.2     *cost of land (M$)",  #COST
         "Cost exponent for scaling in 2015 costs model":"costexp=0.8     *cost exponent for scaling in 2015 costs model",  #COST
         "Cost exponent for pebbles in 2015 costs model":"costexp_pebbles=0.6     *cost exponent for pebbles in 2015 costs model",  #COST
         "Cost scaling factor for buildings":"cost_factor_buildings=1     *cost scaling factor for buildings",  #COST
         "Cost scaling factor for land":"cost_factor_land=1     *cost scaling factor for land",  #COST
         "Cost scaling factor for TF coils":"cost_factor_tf_coils=1     *cost scaling factor for TF coils",  #COST
         "Cost scaling factor for fwbs":"cost_factor_fwbs=1     *cost scaling factor for fwbs",  #COST
         "Cost scaling factor for remote handling":"cost_factor_rh=1     *cost scaling factor for remote handling",  #COST
         "Cost scaling factor for vacuum vessel":"cost_factor_vv=1     *cost scaling factor for vacuum vessel",  #COST
         "Cost scaling factor for energy conversion system":"cost_factor_bop=1     *cost scaling factor for energy conversion system",  #COST
         "Cost scaling factor for remaining subsystems":"cost_factor_misc=1     *cost scaling factor for remaining subsystems",  #COST
         "Maintenance cost factor: first wall, blanket, shield, divertor":"maintenance_fwbs=0.2     *Maintenance cost factor: first wall, blanket, shield, divertor",  #COST
         "Maintenance cost factor: All other components except coils, vacuum vessel, thermal shield, cryostat, land":"maintenance_gen=0.05     *Maintenance cost factor: All other components except coils, vacuum vessel, thermal shield, cryostat, land",  #COST
         "Amortization factor (fixed charge factor) 'A' (years)":"amortization=13.6     *amortization factor (fixed charge factor) 'A' (years)",  #COST
         "Switch for cost model:":"cost_model=1     *Switch for cost model:",  #COST
         "Owner cost factor":"cowner=0.15     *owner cost factor",  #COST
         "User input full power year lifetime of the centrepost (years) (i_cp_lifetime = 0)":"cplife_input=2     *User input full power year lifetime of the centrepost (years) (i_cp_lifetime = 0)",  #COST
         "Allowable ST centrepost neutron fluence (MW-yr/m2)":"cpstflnc=10     *allowable ST centrepost neutron fluence (MW-yr/m2)",  #COST
         "Allowance for site costs (M$)":"csi=16     *allowance for site costs (M$)",  #COST
         "Cost of turbine building (M$)":"cturbb=38     *cost of turbine building (M$)",  #COST
         "Proportion of constructed cost required for decommissioning fund":"decomf=0.1     *proportion of constructed cost required for decommissioning fund",  #COST
         "Average cost of money for construction of plant assuming design/construction time of six years":"fcap0=1.165     *average cost of money for construction of plant assuming design/construction time of six years",  #COST
         "Average cost of money for replaceable components assuming lead time for these of two years":"fcap0cp=1.08     *average cost of money for replaceable components assuming lead time for these of two years",  #COST
         "Fraction of current drive cost treated as fuel (if ifueltyp = 1)":"fcdfuel=0.1     *fraction of current drive cost treated as fuel (if ifueltyp = 1)",  #COST
         "Project contingency factor":"fcontng=0.195     *project contingency factor",  #COST
         "Fixed charge rate during construction":"fcr0=0.0966     *fixed charge rate during construction",  #COST
         "Multiplier for Nth of a kind costs":"fkind=1     *multiplier for Nth of a kind costs",  #COST
         "Switch for plant availability model:":"iavail=2     *Switch for plant availability model:",  #COST
         "Allowable DPA from DEMO fw/blanket lifetime calculation in availability module":"life_dpa=50     *Allowable DPA from DEMO fw/blanket lifetime calculation in availability module",  #COST
         "Number of fusion cycles to reach allowable DPA from DEMO fw/blanket lifetime calculation":"bktcycles=1000     *Number of fusion cycles to reach allowable DPA from DEMO fw/blanket lifetime calculation",  #COST
         "Minimum availability (constraint equation 61)":"avail_min=0.75     *Minimum availability (constraint equation 61)",  #COST
         "Unit cost for tokamak complex buildings, including building and site services ($/m3)":"tok_build_cost_per_vol=1283     *Unit cost for tokamak complex buildings, including building and site services ($/m3)",  #COST
         "Unit cost for unshielded non-active buildings ($/m3)":"light_build_cost_per_vol=270     *Unit cost for unshielded non-active buildings ($/m3)",  #COST
         "F-value for minimum availability (constraint equation 61)":"favail=1     *F-value for minimum availability (constraint equation 61)",  #COST
         "Number of remote handling systems (1-10)":"num_rh_systems=4     *Number of remote handling systems (1-10)",  #COST
         "C parameter, which determines the temperature margin at which magnet lifetime starts to decline":"conf_mag=0.99     *c parameter, which determines the temperature margin at which magnet lifetime starts to decline",  #COST
         "Divertor probability of failure (per op day)":"div_prob_fail=0.0002     *Divertor probability of failure (per op day)",  #COST
         "Divertor unplanned maintenance time (years)":"div_umain_time=0.25     *Divertor unplanned maintenance time (years)",  #COST
         "Reference value for cycle cycle life of divertor":"div_nref=7000     *Reference value for cycle cycle life of divertor",  #COST
         "The cycle when the divertor fails with 100% probability":"div_nu=14000     *The cycle when the divertor fails with 100% probability",  #COST
         "Reference value for cycle life of blanket":"fwbs_nref=20000     *Reference value for cycle life of blanket",  #COST
         "The cycle when the blanket fails with 100% probability":"fwbs_nu=40000     *The cycle when the blanket fails with 100% probability",  #COST
         "Fwbs probability of failure (per op day)":"fwbs_prob_fail=0.0002     *Fwbs probability of failure (per op day)",  #COST
         "Fwbs unplanned maintenance time (years)":"fwbs_umain_time=0.25     *Fwbs unplanned maintenance time (years)",  #COST
         "Vacuum system pump redundancy level (%)":"redun_vacp=25     *Vacuum system pump redundancy level (%)",  #COST
         "Time taken to replace blanket (y) (iavail=1)":"tbktrepl=0.5     *time taken to replace blanket (y) (iavail=1)",  #COST
         "Time taken to replace both blanket and divertor (y) (iavail=1)":"tcomrepl=0.5     *time taken to replace both blanket and divertor (y) (iavail=1)",  #COST
         "Time taken to replace divertor (y) (iavail=1)":"tdivrepl=0.25     *time taken to replace divertor (y) (iavail=1)",  #COST
         "Unplanned unavailability factor for balance of plant (iavail=1)":"uubop=0.02     *unplanned unavailability factor for balance of plant (iavail=1)",  #COST
         "Unplanned unavailability factor for current drive (iavail=1)":"uucd=0.02     *unplanned unavailability factor for current drive (iavail=1)",  #COST
         "Unplanned unavailability factor for divertor (iavail=1)":"uudiv=0.04     *unplanned unavailability factor for divertor (iavail=1)",  #COST
         "Unplanned unavailability factor for fuel system (iavail=1)":"uufuel=0.02     *unplanned unavailability factor for fuel system (iavail=1)",  #COST
         "Unplanned unavailability factor for first wall (iavail=1)":"uufw=0.04     *unplanned unavailability factor for first wall (iavail=1)",  #COST
         "Unplanned unavailability factor for magnets (iavail=1)":"uumag=0.02     *unplanned unavailability factor for magnets (iavail=1)",  #COST
         "Unplanned unavailability factor for vessel (iavail=1)":"uuves=0.04     *unplanned unavailability factor for vessel (iavail=1)",  #COST
         "Switch for net electric power and cost of electricity calculations:":"ireactor=1     *Switch for net electric power and cost of electricity calculations:",  #COST
         "Level of safety assurance switch (generally, use 3 or 4):":"lsa=4     *Level of safety assurance switch (generally, use 3 or 4):",  #COST
         "Switch for costs output:":"output_costs=1     *Switch for costs output:",  #COST
         "Effective cost of money in constant dollars":"discount_rate=0.0435     *effective cost of money in constant dollars",  #COST
         "Ratio of additional HCD power for start-up to flat-top operational requirements":"startupratio=1     *ratio of additional HCD power for start-up to flat-top operational requirements",  #COST
         "Full power year plant lifetime (years)":"tlife=30     *Full power year plant lifetime (years)",  #COST
         "Unit cost for administration buildings (M$/m3)":"ucad=180.0D0     *unit cost for administration buildings (M$/m3)",  #COST
         "Unit cost for aux facility power equipment ($)":"ucaf=1.5D6     *unit cost for aux facility power equipment ($)",  #COST
         "Unit cost for aux heat transport equipment ($/W**exphts)":"ucahts=31.0D0     *unit cost for aux heat transport equipment ($/W**exphts)",  #COST
         "Unit cost of auxiliary transformer ($/kVA)":"ucap=17.0D0     *unit cost of auxiliary transformer ($/kVA)",  #COST
         "Unit cost for blanket beryllium ($/kg)":"ucblbe=260     *unit cost for blanket beryllium ($/kg)",  #COST
         "Unit cost for breeder material ($/kg) (blktmodel>0)":"ucblbreed=875     *unit cost for breeder material ($/kg) (blktmodel>0)",  #COST
         "Unit cost for blanket lithium ($/kg) (30% Li6)":"ucblli=875     *unit cost for blanket lithium ($/kg) (30% Li6)",  #COST
         "Unit cost for blanket Li_2O ($/kg)":"ucblli2o=600     *unit cost for blanket Li_2O ($/kg)",  #COST
         "Unit cost for blanket Li-Pb ($/kg) (30% Li6)":"ucbllipb=10.3     *unit cost for blanket Li-Pb ($/kg) (30% Li6)",  #COST
         "Unit cost for blanket stainless steel ($/kg)":"ucblss=90     *unit cost for blanket stainless steel ($/kg)",  #COST
         "Unit cost for blanket vanadium ($/kg)":"ucblvd=200     *unit cost for blanket vanadium ($/kg)",  #COST
         "Vacuum system backing pump cost ($)":"ucbpmp=2.925D5     *vacuum system backing pump cost ($)",  #COST
         "Cost of aluminium bus for TF coil ($/A-m)":"ucbus=0.123     *cost of aluminium bus for TF coil ($/A-m)",  #COST
         "Cost of superconductor case ($/kg)":"uccase=50     *cost of superconductor case ($/kg)",  #COST
         "Unit cost for control buildings (M$/m3)":"ucco=350.0D0     *unit cost for control buildings (M$/m3)",  #COST
         "Cost of high strength tapered copper ($/kg)":"uccpcl1=250     *cost of high strength tapered copper ($/kg)",  #COST
         "Cost of TF outboard leg plate coils ($/kg)":"uccpclb=150     *cost of TF outboard leg plate coils ($/kg)",  #COST
         "Vacuum system cryopump cost ($)":"uccpmp=3.9D5     *vacuum system cryopump cost ($)",  #COST
         "Unit cost for cryogenic building (M$/vol)":"uccr=460.0D0     *unit cost for cryogenic building (M$/vol)",  #COST
         "Heat transport system cryoplant costs ($/W**expcry)":"uccry=93000     *heat transport system cryoplant costs ($/W**expcry)",  #COST
         "Unit cost for vacuum vessel ($/kg)":"uccryo=32     *unit cost for vacuum vessel ($/kg)",  #COST
         "Unit cost for copper in superconducting cable ($/kg)":"uccu=75     *unit cost for copper in superconducting cable ($/kg)",  #COST
         "Cost per 8 MW diesel generator ($)":"ucdgen=1.7D6     *cost per 8 MW diesel generator ($)",  #COST
         "Cost of divertor blade ($)":"ucdiv=280000     *cost of divertor blade ($)",  #COST
         "Detritiation, air cleanup cost ($/10000m3/hr)":"ucdtc=13.0D0     *detritiation, air cleanup cost ($/10000m3/hr)",  #COST
         "Vacuum system duct cost ($/m)":"ucduct=4.225D4     *vacuum system duct cost ($/m)",  #COST
         "ECH system cost ($/W)":"ucech=3     *ECH system cost ($/W)",  #COST
         "Unit cost for electrical equipment building (M$/m3)":"ucel=380.0D0     *unit cost for electrical equipment building (M$/m3)",  #COST
         "MGF (motor-generator flywheel) cost factor ($/MVA**0.8)":"uces1=3.2D4     *MGF (motor-generator flywheel) cost factor ($/MVA**0.8)",  #COST
         "MGF (motor-generator flywheel) cost factor ($/MJ**0.8)":"uces2=8.8D3     *MGF (motor-generator flywheel) cost factor ($/MJ**0.8)",  #COST
         "Cost of fuelling system ($)":"ucf1=22300000     *cost of fuelling system ($)",  #COST
         "Outer PF coil fence support cost ($/kg)":"ucfnc=35     *outer PF coil fence support cost ($/kg)",  #COST
         "Cost of 60g/day tritium processing unit ($)":"ucfpr=4.4D7     *cost of 60g/day tritium processing unit ($)",  #COST
         "Unit cost of D-T fuel (M$/year/1200MW)":"ucfuel=3.45     *unit cost of D-T fuel (M$/year/1200MW)",  #COST
         "First wall armour cost ($/m2)":"ucfwa=6.0D4     *first wall armour cost ($/m2)",  #COST
         "First wall passive stabiliser cost ($)":"ucfwps=1.0D7     *first wall passive stabiliser cost ($)",  #COST
         "First wall structure cost ($/m2)":"ucfws=5.3D4     *first wall structure cost ($/m2)",  #COST
         "Cost of reactor structure ($/kg)":"ucgss=35.0D0     *cost of reactor structure ($/kg)",  #COST
         "Cost of helium-3 ($/kg)":"uche3=1000000     *cost of helium-3 ($/kg)",  #COST
         "Cost of heat rejection system ($)":"uchrs=87900000     *cost of heat rejection system ($)",  #COST
         "Cost of heat transport system equipment per loop ($/W); dependent on coolant type (coolwh)":"uchts=[15.3 19.1]     *cost of heat transport system equipment per loop ($/W); dependent on coolant type (coolwh)",  #COST
         "Cost of instrumentation, control & diagnostics ($)":"uciac=150000000     *cost of instrumentation, control & diagnostics ($)",  #COST
         "ICH system cost ($/W)":"ucich=3     *ICH system cost ($/W)",  #COST
         "Superconductor intercoil structure cost ($/kg)":"ucint=35.0D0     *superconductor intercoil structure cost ($/kg)",  #COST
         "Lower hybrid system cost ($/W)":"uclh=3.3     *lower hybrid system cost ($/W)",  #COST
         "Low voltage system cost ($/kVA)":"uclv=16.0D0     *low voltage system cost ($/kVA)",  #COST
         "Unit cost for reactor maintenance building (M$/m3)":"ucmb=260.0D0     *unit cost for reactor maintenance building (M$/m3)",  #COST
         "Cost of maintenance equipment ($)":"ucme=125000000     *cost of maintenance equipment ($)",  #COST
         "Miscellaneous plant allowance ($)":"ucmisc=25000000     *miscellaneous plant allowance ($)",  #COST
         "NBI system cost ($/W)":"ucnbi=3.3     *NBI system cost ($/W)",  #COST
         "Cost of nuclear building ventilation ($/m3)":"ucnbv=1000.0D0     *cost of nuclear building ventilation ($/m3)",  #COST
         "Annual cost of operation and maintenance (M$/year/1200MW**0.5)":"ucoam=[68.8 68.8 68.8 74.4]     *annual cost of operation and maintenance (M$/year/1200MW**0.5)",  #COST
         "Penetration shield cost ($/kg)":"ucpens=32     *penetration shield cost ($/kg)",  #COST
         "Cost of PF coil buses ($/kA-m)":"ucpfb=210     *cost of PF coil buses ($/kA-m)",  #COST
         "Cost of PF coil DC breakers ($/MVA**0.7)":"ucpfbk=16600     *cost of PF coil DC breakers ($/MVA**0.7)",  #COST
         "Cost of PF burn power supplies ($/kW**0.7)":"ucpfbs=4900     *cost of PF burn power supplies ($/kW**0.7)",  #COST
         "Cost of PF coil AC breakers ($/circuit)":"ucpfcb=75000     *cost of PF coil AC breakers ($/circuit)",  #COST
         "Cost factor for dump resistors ($/MJ)":"ucpfdr1=150     *cost factor for dump resistors ($/MJ)",  #COST
         "Cost of PF instrumentation and control ($/channel)":"ucpfic=10000     *cost of PF instrumentation and control ($/channel)",  #COST
         "Cost of PF coil pulsed power supplies ($/MVA)":"ucpfps=35000     *cost of PF coil pulsed power supplies ($/MVA)",  #COST
         "Primary heat transport cost ($/W**exphts)":"ucphx=15.0D0     *primary heat transport cost ($/W**exphts)",  #COST
         "Cost of primary power transformers ($/kVA**0.9)":"ucpp=48.0D0     *cost of primary power transformers ($/kVA**0.9)",  #COST
         "Cost of reactor building (M$/m3)":"ucrb=400     *cost of reactor building (M$/m3)",  #COST
         "Cost of superconductor ($/kg)":"ucsc=[ 600. 600. 300. 600. 600. 600. 300. 1200. 1200.]     *cost of superconductor ($/kg)",  #COST
         "Cost of shops and warehouses (M$/m3)":"ucsh=115.0D0     *cost of shops and warehouses (M$/m3)",  #COST
         "Cost of shield structural steel ($/kg)":"ucshld=32     *cost of shield structural steel ($/kg)",  #COST
         "Switchyard equipment costs ($)":"ucswyd=1.84D7     *switchyard equipment costs ($)",  #COST
         "Cost of TF coil breakers ($/W**0.7)":"uctfbr=1.22     *cost of TF coil breakers ($/W**0.7)",  #COST
         "Cost of TF coil bus ($/kg)":"uctfbus=100     *cost of TF coil bus ($/kg)",  #COST
         "Cost of TF coil dump resistors ($/J)":"uctfdr=1.75D-4     *cost of TF coil dump resistors ($/J)",  #COST
         "Additional cost of TF coil dump resistors ($/coil)":"uctfgr=5000.0D0     *additional cost of TF coil dump resistors ($/coil)",  #COST
         "Cost of TF coil instrumentation and control ($/coil/30)":"uctfic=1.0D4     *cost of TF coil instrumentation and control ($/coil/30)",  #COST
         "Cost of TF coil power supplies ($/W**0.7)":"uctfps=24     *cost of TF coil power supplies ($/W**0.7)",  #COST
         "Cost of TF coil slow dump switches ($/A)":"uctfsw=1     *cost of TF coil slow dump switches ($/A)",  #COST
         "Cost of turbomolecular pump ($)":"uctpmp=1.105D5     *cost of turbomolecular pump ($)",  #COST
         "Cost of tritium building ($/m3)":"uctr=370.0D0     *cost of tritium building ($/m3)",  #COST
         "Cost of turbine plant equipment ($) (dependent on coolant type coolwh)":"ucturb=[2.30e+08 2.45e+08]     *cost of turbine plant equipment ($) (dependent on coolant type coolwh)",  #COST
         "Vacuum system valve cost ($)":"ucvalv=3.9D5     *vacuum system valve cost ($)",  #COST
         "Vacuum duct shield cost ($/kg)":"ucvdsh=26.0D0     *vacuum duct shield cost ($/kg)",  #COST
         "Vacuum system instrumentation and control cost ($)":"ucviac=1.3D6     *vacuum system instrumentation and control cost ($)",  #COST
         "Cost of PF coil superconductor windings ($/m)":"ucwindpf=465     *cost of PF coil superconductor windings ($/m)",  #COST
         "Cost of TF coil superconductor windings ($/m)":"ucwindtf=480     *cost of TF coil superconductor windings ($/m)",  #COST
         "Cost of active assembly shop ($/m3)":"ucws=460.0D0     *cost of active assembly shop ($/m3)",  #COST
         "Cost of waste disposal (M$/y/1200MW)":"ucwst=[0. 3.94 5.91 7.88]     *cost of waste disposal (M$/y/1200MW)",  #COST

    }
    create_checkboxes("Select Cost Variables", Cost_variables_values, 'Cost_variables')
    

#Current Drive Function
def Current_drive_variables():
    """Display a list of checkboxes for the user to select Current Drive Variables, with a scrollbar."""
    Current_drive_variables_values = {
         "Width of neutral beam duct where it passes between the TF coils (m) ":"beamwd=0.58     *width of neutral beam duct where it passes between the TF coils (m) ",  #Current Drive
         "Maximum fraction of plasma current from bootstrap; if bscfmax < 0, bootstrap fraction = abs(bscfmax)":"bscfmax=0.9     *maximum fraction of plasma current from bootstrap; if bscfmax < 0, bootstrap fraction = abs(bscfmax)",  #Current Drive
         "Bootstrap current fraction multiplier (ibss=1)":"cboot=0.9     *bootstrap current fraction multiplier (ibss=1)",  #Current Drive
         "Cyclotron harmonic frequency number, used in cut-off function":"harnum=0.9     *cyclotron harmonic frequency number, used in cut-off function",  #Current Drive
         "Neutral beam energy (keV) (iteration variable 19)":"enbeam=1000     *neutral beam energy (keV) (iteration variable 19)",  #Current Drive
         "ECH wall plug to injector efficiency":"etaech=0.3     *ECH wall plug to injector efficiency",  #Current Drive
         "Lower hybrid wall plug to injector efficiency":"etalh=0.3     *lower hybrid wall plug to injector efficiency",  #Current Drive
         "Neutral beam wall plug to injector efficiency":"etanbi=0.3     *neutral beam wall plug t    o injector efficiency",  #Current Drive
         "Fraction of beam energy to ions":"fpion=0.5     *fraction of beam energy to ions",  #Current Drive
         "Current drive efficiency fudge factor (iteration variable 47)":"feffcd=1     *current drive efficiency fudge factor (iteration variable 47)",  #Current Drive
         "R_tangential / R_major for neutral beam injection":"frbeam=1.05     *R_tangential / R_major for neutral beam injection",  #Current Drive
         "Fraction of beam that is tritium":"ftritbm=1.00E-06     *fraction of beam that is tritium",  #Current Drive
         "User input ECRH gamma (1.0e20 A/(W m^2))":"gamma_ecrh=0.35     *User input ECRH gamma (1.0e20 A/(W m^2))",  #Current Drive
         "User scaling input for EBW plasma heating. Default 0.43":"xi_ebw=0.8     *User scaling input for EBW plasma heating. Default 0.43",  #Current Drive
         "Switch for current drive efficiency model:":"iefrf=5     *Switch for current drive efficiency model:",  #Current Drive
         "Switch for current drive calculation:":"irfcd=1     *Switch for current drive calculation:",  #Current Drive
         "Neutral beam duct shielding thickness (m)":"nbshield=0.5     *neutral beam duct shielding thickness (m)",  #Current Drive
         "Maximum allowable value for injected power (MW) (constraint equation 30)":"pinjalw=150     *maximum allowable value for injected power (MW) (constraint equation 30)",  #Current Drive
         "Permitted neutral beam e-decay lengths to plasma centre":"tbeamin=3     *permitted neutral beam e-decay lengths to plasma centre",  #Current Drive

    }
    create_checkboxes("Select Current Drive", Current_drive_variables_values, 'Current_drive')

#Divertor Variable Function
def Divertor_variables():
    """Display a list of checkboxes for the user to select Divertor Variables, with a scrollbar."""
    Divertor_values = {
         "Angle of incidence of field line on plate (rad)":"anginc=0.262     *angle of incidence of field line on plate (rad)",  #Divertor
         "Field line angle wrt divertor target plate (degrees)":"beta_div=1     *field line angle wrt divertor target plate (degrees)",  #Divertor
         "Poloidal plane angle between divertor plate and leg, inboard (rad)":"betai=1     *poloidal plane angle between divertor plate and leg, inboard (rad)",  #Divertor
         "Poloidal plane angle between divertor plate and leg, outboard (rad)":"betao=1     *poloidal plane angle between divertor plate and leg, outboard (rad)",  #Divertor
         "Reference B_p at outboard divertor strike point (T)":"bpsout=0.6     *reference B_p at outboard divertor strike point (T)",  #Divertor
         "Fitting coefficient to adjust ptpdiv, ppdiv": {
          "c1div=0.45":"c1div=0.45     *fitting coefficient to adjust ptpdiv, ppdiv",
          "c2div=-7":"c2div=-7     *fitting coefficient to adjust ptpdiv, ppdiv", 
          "c3div=0.54":"c3div=0.54     *fitting coefficient to adjust ptpdiv, ppdiv", 
          "c4div=-3.6":"c4div=-3.6     *fitting coefficient to adjust ptpdiv, ppdiv", 
          "c5div=0.7":"c5div=0.7     *fitting coefficient to adjust ptpdiv, ppdiv", 
         },
         "Coeff for power distribution along main plasma":"delld=1     *coeff for power distribution along main plasma",  #Divertor
         "Divertor coolant fraction":"divclfr=0.3     *divertor coolant fraction",  #Divertor
         "Divertor structure density (kg/m3)":"divdens=10000     *divertor structure density (kg/m3)",  #Divertor
         "Divertor structure vertical thickness (m)":"divfix=0.2     *divertor structure vertical thickness (m)",  #Divertor
         "Divertor plate thickness (m) (from Spears, Sept 1990)":"divplt=0.035     *divertor plate thickness (m) (from Spears, Sept 1990)",  #Divertor
         "Radial gradient ratio":"fdfs=10     *radial gradient ratio",  #Divertor
         "Divertor area fudge factor (for ITER, Sept 1990)":"fdiva=1.11     *divertor area fudge factor (for ITER, Sept 1990)",  #Divertor
         "Coefficient for gamdiv":"fififi=0.004     *coefficient for gamdiv",  #Divertor
         "The plasma flux expansion in the divertor (default 2; Wade 2020)":"flux_exp=2     *The plasma flux expansion in the divertor (default 2; Wade 2020)",  #Divertor
         "Fraction of radiated power to plate":"frrp=0.4     *fraction of radiated power to plate",  #Divertor
         "Heat load limit (MW/m2)":"hldivlim=5     *heat load limit (MW/m2)",  #Divertor
         "Power fraction for outboard double-null scrape-off plasma":"ksic=0.8     *power fraction for outboard double-null scrape-off plasma",  #Divertor
         "Pressure ratio (nT)_plasma / (nT)_scrape-off":"omegan=1     *pressure ratio (nT)_plasma / (nT)_scrape-off",  #Divertor
         "N-scrape-off / n-average plasma; (input for ipedestal=0, = nesep/dene if ipedestal>=1)":"prn1=0.285     *n-scrape-off / n-average plasma; (input for ipedestal=0, = nesep/dene if ipedestal>=1)",  #Divertor
         "Maximum value for length ratio (rlclolcn) (constraintg eqn 22)":"rlenmax=0.5     *maximum value for length ratio (rlclolcn) (constraintg eqn 22)",  #Divertor
         "Temperature at divertor (eV) (input for stellarator only, calculated for tokamaks)":"tdiv=2     *temperature at divertor (eV) (input for stellarator only, calculated for tokamaks)",  #Divertor
         "Parallel heat transport coefficient (m2/s)":"xparain=2100     *parallel heat transport coefficient (m2/s)",  #Divertor
         "Perpendicular heat transport coefficient (m2/s)":"xpertin=2     *perpendicular heat transport coefficient (m2/s)",  #Divertor
         "Zeff in the divertor region (if divdum/=0)":"zeffdiv=1     *Zeff in the divertor region (if divdum/=0)",  #Divertor

    }
    create_checkboxes("Select Divertor Variable", Divertor_values, 'Divertor_values')

#Fwbs Encapsule Function
def Fwbs_variables():
    """Display a list of checkboxes for the user to select Fwbs Variables, with a scrollbar."""
    Fwbs_values = {
        "Full power blanket lifetime (years)":"bktlife=     *Full power blanket lifetime (years)",  #Fwbs 
        "Mass of water coolant (in shield, blanket, first wall, divertor) [kg]":"coolmass=     *mass of water coolant (in shield, blanket, first wall, divertor) [kg]",  #Fwbs 
        "Vacuum vessel mass [kg]":"vvmass=     *vacuum vessel mass [kg]",  #Fwbs 
        "Density of steel [kg m^-3]":"denstl=7800     *density of steel [kg m^-3]",  #Fwbs 
        "Density of tungsten [kg m^-3]":"denw=19250     *density of tungsten [kg m^-3]",  #Fwbs 
        "Density of tungsten carbide [kg m^-3]":"denwc=15630     *density of tungsten carbide [kg m^-3]",  #Fwbs 
        "Total mass of vacuum vessel + cryostat [kg] (calculated if blktmodel>0)":"dewmkg=     *total mass of vacuum vessel + cryostat [kg] (calculated if blktmodel>0)",  #Fwbs 
        "Energy multiplication in blanket and shield":"emult=1.269     *energy multiplication in blanket and shield",  #Fwbs 
        "Power due to energy multiplication in blanket and shield [MW]":"emultmw=     *power due to energy multiplication in blanket and shield [MW]",  #Fwbs 
        "KIT blanket model: steel fraction of breeding zone":"fblss=0.09705     *KIT blanket model: steel fraction of breeding zone",  #Fwbs 
        "Solid angle fraction taken by one divertor":"fdiv=0.115     *Solid angle fraction taken by one divertor",  #Fwbs 
        "Area fraction covered by heating/current drive apparatus plus diagnostics":"fhcd=     *area fraction covered by heating/current drive apparatus plus diagnostics",  #Fwbs 
        "Area fraction taken up by other holes (IFE)":"fhole=     *area fraction taken up by other holes (IFE)",  #Fwbs 
        
        "Switch for first wall, blanket, shield and vacuum vessel shape:":{
           "=2 Default":"fwbsshape=2     *0",  #Fwbs 
           "=1 D-shaped (cylinder inboard + ellipse outboard)":"fwbsshape=1     *=1 D-shaped (cylinder inboard + ellipse outboard)",  #Fwbs 
           "=2 defined by two ellipses":"fwbsshape=2     *=2 defined by two ellipses",  #Fwbs 
        },
        "First wall full-power year lifetime (y)":"fwlife=     *first wall full-power year lifetime (y)",  #Fwbs 
        "First wall mass [kg]":"fwmass=     *first wall mass [kg]",  #Fwbs 
        "First wall armour mass [kg]":"fw_armour_mass=     *first wall armour mass [kg]",  #Fwbs 
        "First wall armour thickness [m]":"fw_armour_thickness=0.005     *first wall armour thickness [m]",  #Fwbs 
        "First wall armour volume [m^3]":"fw_armour_vol=     *first wall armour volume [m^3]",  #Fwbs 
        "Switch for blanket model:":{
          "=1 Default":"iblanket=1     *0",  #Fwbs 
          "=1 CCFE HCPB model":"iblanket=1     *=1 CCFE HCPB model",  #Fwbs 
          "=2 KIT HCPB model # REMOVED, no longer usable":"iblanket=2     *=2 KIT HCPB model # REMOVED, no longer usable",  #Fwbs 
          "=3 CCFE HCPB model with Tritium Breeding Ratio calculation":"iblanket=3     *=3 CCFE HCPB model with Tritium Breeding Ratio calculation",  #Fwbs 
          "=4 KIT HCLL model # REMOVED, no longer usable":"iblanket=4     *=4 KIT HCLL model # REMOVED, no longer usable",  #Fwbs 
          "=5 DCLL model - no nutronics model included (in development) please check/choose values for 'dual-coolant blanket' fractions (provided in this file). - please use primary_pumping = 0 or 1.":"iblanket=5     *=5 DCLL model - no nutronics model included (in development) please check/choose values for 'dual-coolant blanket' fractions (provided in this file). - please use primary_pumping = 0 or 1.",  #Fwbs 
        }, 
        "Switch for inboard blanket:":{
          "=1 Default":"iblnkith=1     *0",  #Fwbs 
          "=0 No inboard blanket (blnkith=0.0)":"iblnkith=0     *=0 No inboard blanket (blnkith=0.0)",  #Fwbs 
          "=1 Inboard blanket present":"iblnkith=1     *=1 Inboard blanket present",  #Fwbs 
        },
        "Switch for nuclear heating in the coils:":{
          "=0 Frances Fox model (default)":"inuclear=0     *=0 Frances Fox model (default)",  #Fwbs 
          "=1 Fixed by user (qnuc)":"inuclear=1     *=1 Fixed by user (qnuc)",  #Fwbs 
        },
        "Nuclear heating in the coils (W) (inuclear=1)":"qnuc=     *nuclear heating in the coils (W) (inuclear=1)",  #Fwbs 
        "Lithium-6 enrichment of breeding material (%)":"li6enrich=30     *lithium-6 enrichment of breeding material (%)",  #Fwbs 
        "Nuclear heating in the blanket [MW]":"pnucblkt=     *nuclear heating in the blanket [MW]",  #Fwbs 
        "Total nuclear heating in the ST centrepost [MW]":"pnuc_cp=     *Total nuclear heating in the ST centrepost [MW]",  #Fwbs 
        "Neutronic shield nuclear heating in the ST centrepost [MW]":"pnuc_cp_sh=     *Neutronic shield nuclear heating in the ST centrepost [MW]",  #Fwbs 
        "TF neutronic nuclear heating in the ST centrepost [MW]":"pnuc_cp_tf=     *TF neutronic nuclear heating in the ST centrepost [MW]",  #Fwbs 
        "Nuclear heating in the divertor [MW]":"pnucdiv=     *nuclear heating in the divertor [MW]",  #Fwbs 
        "Nuclear heating in the first wall [MW]":"pnucfw=     *nuclear heating in the first wall [MW]",  #Fwbs 
        "Nuclear heating in the HCD apparatus and diagnostics [MW]":"pnuchcd=     *nuclear heating in the HCD apparatus and diagnostics [MW]",  #Fwbs 
        "Nuclear heating lost via holes [MW]":"pnucloss=     *nuclear heating lost via holes [MW]",  #Fwbs 
        "Nuclear heating to vacuum vessel and beyond [MW]":"pnucvvplus=     *nuclear heating to vacuum vessel and beyond [MW]",  #Fwbs 
        "Nuclear heating in the shield [MW]":"pnucshld=     *nuclear heating in the shield [MW]",  #Fwbs 
        "Mass of blanket [kg]":"whtblkt=     *mass of blanket [kg]",  #Fwbs 
        "Mass of blanket - steel part [kg]":"whtblss=     *mass of blanket - steel part [kg]",  #Fwbs 
        "Total mass of armour, first wall and blanket [kg]":"armour_fw_bl_mass=     *Total mass of armour, first wall and blanket [kg]",  #Fwbs 
        "Volume ratio: Li4SiO4/(Be12Ti+Li4SiO4) (iteration variable 108)":"breeder_f=0.5     *Volume ratio: Li4SiO4/(Be12Ti+Li4SiO4) (iteration variable 108)",  #Fwbs 
        "Combined breeder/multipler fraction of blanket by volume":"breeder_multiplier=0.75     *combined breeder/multipler fraction of blanket by volume",  #Fwbs 
        "He coolant fraction of blanket by volume (iblanket= 1,3 (CCFE HCPB))":"vfcblkt=0.05295     *He coolant fraction of blanket by volume (iblanket= 1,3 (CCFE HCPB))",  #Fwbs 
        "He purge gas fraction of blanket by volume (iblanket= 1,3 (CCFE HCPB))":"vfpblkt=0.1     *He purge gas fraction of blanket by volume (iblanket= 1,3 (CCFE HCPB))",  #Fwbs 
        "Mass of lithium orthosilicate in blanket [kg] (iblanket=1,3 (CCFE HCPB))":"whtblli4sio4=     *mass of lithium orthosilicate in blanket [kg] (iblanket=1,3 (CCFE HCPB))",  #Fwbs 
        "Mass of titanium beryllide in blanket [kg] (iblanket=1,3 (CCFE HCPB))":"whtbltibe12=     *mass of titanium beryllide in blanket [kg] (iblanket=1,3 (CCFE HCPB))",  #Fwbs 

        "Inboard/outboard FW coolant void fraction":"vffwi=     *Inboard/outboard FW coolant void fraction",  #Fwbs 
        "Inboard/outboard FW coolant void fraction":"vffwo=     *Inboard/outboard FW coolant void fraction",  #Fwbs 
        "Surface heat flux on first wall [MW] (sum = pradfw)":"psurffwi=     *Surface heat flux on first wall [MW] (sum = pradfw)",  #Fwbs 
        "Surface heat flux on first wall [MW] (sum = pradfw)":"psurffwo=     *Surface heat flux on first wall [MW] (sum = pradfw)",  #Fwbs 
        "First wall volume [m3]":"volfw=     *First wall volume [m3]",  #Fwbs 
        "Fractions of blanket by volume: steel, lithium orthosilicate, titanium beryllide":"fblss_ccfe=     *Fractions of blanket by volume: steel, lithium orthosilicate, titanium beryllide",  #Fwbs 
        "Fractions of blanket by volume: steel, lithium orthosilicate, titanium beryllide":"fblli2sio4=     *Fractions of blanket by volume: steel, lithium orthosilicate, titanium beryllide",  #Fwbs 
        "Fractions of blanket by volume: steel, lithium orthosilicate, titanium beryllide":"fbltibe12=     *Fractions of blanket by volume: steel, lithium orthosilicate, titanium beryllide",  #Fwbs 
        
        "Breeder material switch (iblanket=2 (KIT HCPB)):":{
          "=1 Default":"breedmat=1     *0",  #Fwbs 
          "=1 Lithium orthosilicate":"breedmat=1     *=1 Lithium orthosilicate",  #Fwbs 
          "=2 Lithium methatitanate":"breedmat=2     *=2 Lithium methatitanate",  #Fwbs 
          "=3 Lithium zirconate":"breedmat=3     *=3 Lithium zirconate",  #Fwbs 
        }, 
        "Density of breeder material [kg m^-3] (iblanket=2 (KIT HCPB))":"densbreed=     *density of breeder material [kg m^-3] (iblanket=2 (KIT HCPB))",  #Fwbs 
        "Beryllium fraction of blanket by volume (if iblanket=2, is Be fraction of breeding zone)":"fblbe=0.6     *beryllium fraction of blanket by volume (if iblanket=2, is Be fraction of breeding zone)",  #Fwbs 
        "Breeder fraction of blanket breeding zone by volume (iblanket=2 (KIT HCPB))":"fblbreed=0.154     *breeder fraction of blanket breeding zone by volume (iblanket=2 (KIT HCPB))",  #Fwbs 
        "Helium fraction of inboard blanket box manifold by volume (iblanket=2 (KIT HCPB))":"fblhebmi=0.4     *helium fraction of inboard blanket box manifold by volume (iblanket=2 (KIT HCPB))",  #Fwbs 
        "Helium fraction of outboard blanket box manifold by volume (iblanket=2 (KIT HCPB))":"fblhebmo=0.4     *helium fraction of outboard blanket box manifold by volume (iblanket=2 (KIT HCPB))",  #Fwbs 
        "Helium fraction of inboard blanket back plate by volume (iblanket=2 (KIT HCPB))":"fblhebpi=0.6595     *helium fraction of inboard blanket back plate by volume (iblanket=2 (KIT HCPB))",  #Fwbs 
        "Helium fraction of outboard blanket back plate by volume (iblanket=2 (KIT HCPB))":"fblhebpo=0.6713     *helium fraction of outboard blanket back plate by volume (iblanket=2 (KIT HCPB))",  #Fwbs 
        "switch for size of heating/current drive ports (iblanket=2 (KIT HCPB)):":{ 
          "=1 Default":"hcdportsize=1     *",  #Fwbs 
          "=1 'small'":"hcdportsize=1     *=1 'small'",  #Fwbs 
          "=2 'large'":"hcdportsize=2     *=2 'large'",  #Fwbs 
        },
        "Peak fast neutron fluence on TF coil superconductor [n m^-2] (iblanket=2 (KIT HCPB))":"nflutf=     *peak fast neutron fluence on TF coil superconductor [n m^-2] (iblanket=2 (KIT HCPB))",  #Fwbs 
        "Number of divertor ports (iblanket=2 (KIT HCPB))":"npdiv=2     *number of divertor ports (iblanket=2 (KIT HCPB))",  #Fwbs 
        "Number of inboard ports for heating/current drive (iblanket=2 (KIT HCPB))":"nphcdin=2     *number of inboard ports for heating/current drive (iblanket=2 (KIT HCPB))",  #Fwbs 
        "Number of outboard ports for heating/current drive (iblanket=2 (KIT HCPB))":"nphcdout=2     *number of outboard ports for heating/current drive (iblanket=2 (KIT HCPB))",  #Fwbs 
        "Tritium breeding ratio (iblanket=2,3 (KIT HCPB/HCLL))":"tbr=     *tritium breeding ratio (iblanket=2,3 (KIT HCPB/HCLL))",  #Fwbs 
        "Tritium production rate [g day^-1] (iblanket=2 (KIT HCPB))":"tritprate=     *tritium production rate [g day^-1] (iblanket=2 (KIT HCPB))",  #Fwbs 
        "Neutron wall load peaking factor (iblanket=2 (KIT HCPB))":"wallpf=1.21     *neutron wall load peaking factor (iblanket=2 (KIT HCPB))",  #Fwbs 
        "Mass of blanket - breeder part [kg] (iblanket=2 (KIT HCPB))":"whtblbreed=     *mass of blanket - breeder part [kg] (iblanket=2 (KIT HCPB))",  #Fwbs 
        "Mass of blanket - beryllium part [kg]":"whtblbe=     *mass of blanket - beryllium part [kg]",  #Fwbs 
        "Blanket thickness switch (Do not set blnkith, blnkoth, fwith or fwoth when iblanket=3):":{
          "=2 Default":"iblanket_thickness=2     *0",  #Fwbs 
          "=1 thin 0.53 m inboard, 0.91 m outboard":"iblanket_thickness=1     *=1 thin 0.53 m inboard, 0.91 m outboard",  #Fwbs 
          "=2 medium 0.64 m inboard, 1.11 m outboard":"iblanket_thickness=2     *=2 medium 0.64 m inboard, 1.11 m outboard",  #Fwbs 
          "=3 thick 0.75 m inboard, 1.30 m outboard":"iblanket_thickness=3     *=3 thick 0.75 m inboard, 1.30 m outboard",  #Fwbs 
        }, 
        "Switch for pumping power for primary coolant:":{
          "=2 Default":"primary_pumping=2     *0",  #Fwbs 
          "=0 User sets pump power directly (htpmw_blkt, htpmw_fw, htpmw_div, htpmw_shld)":"primary_pumping=0     *=0 User sets pump power directly (htpmw_blkt, htpmw_fw, htpmw_div, htpmw_shld)",  #Fwbs 
          "=1 User sets pump power as a fraction of thermal power (fpumpblkt, fpumpfw, fpumpdiv, fpumpshld)":"primary_pumping=1     *=1 User sets pump power as a fraction of thermal power (fpumpblkt, fpumpfw, fpumpdiv, fpumpshld)",  #Fwbs 
          "=2 Mechanical pumping power is calculated":"primary_pumping=2     *=2 Mechanical pumping power is calculated",  #Fwbs 
          "=3 Mechanical pumping power is calculated using specified pressure drop":"primary_pumping=3     *=3 Mechanical pumping power is calculated using specified pressure drop",  #Fwbs 
        },
        "Switch for shield material - currently only applied in costing routines cost_model = 2":{
          "=0 Tungsten (default)":"i_shield_mat=0     *=0 Tungsten (default)",  #Fwbs 
          "=1 Tungsten carbide":"i_shield_mat=1     *=1 Tungsten carbide",  #Fwbs 
        },
        "Switch for power conversion cycle:":{
          "=0 Set efficiency for chosen blanket, from detailed models (divertor heat not used)":"secondary_cycle=0     *=0 Set efficiency for chosen blanket, from detailed models (divertor heat not used)",  #Fwbs 
          "=1 Set efficiency for chosen blanket, from detailed models (divertor heat used)":"secondary_cycle=1     *=1 Set efficiency for chosen blanket, from detailed models (divertor heat used)",  #Fwbs 
          "=2 user input thermal-electric efficiency (etath)":"secondary_cycle=2     *=2 user input thermal-electric efficiency (etath)",  #Fwbs 
          "=3 steam Rankine cycle":"secondary_cycle=3     *=3 steam Rankine cycle",  #Fwbs 
          "=4 supercritical CO2 cycle":"secondary_cycle=4     *=4 supercritical CO2 cycle",  #Fwbs 
        },
        "Switch for power conversion cycle for the liquid breeder component of the blanket:":{
          "=4 Default":"secondary_cycle_liq=4     *0",  #Fwbs 
          "=2 user input thermal-electric efficiency (etath)":"secondary_cycle_liq=2     *=2 user input thermal-electric efficiency (etath)",  #Fwbs 
          "=4 supercritical CO2 cycle":"secondary_cycle_liq=4     *=4 supercritical CO2 cycle",  #Fwbs 
        }, 
        "Switch for blanket coolant (set via blkttype):":{
          "=1 Default":"coolwh=1     *0",  #Fwbs 
          "=1 helium":"coolwh=1     *=1 helium",  #Fwbs 
          "=2 pressurized water":"coolwh=2     *=2 pressurized water",  #Fwbs 
        },
        "Inner radius of inboard first wall/blanket coolant channels (stellarator only) [m]":"afwi=0.008     *inner radius of inboard first wall/blanket coolant channels (stellarator only) [m]",  #Fwbs 
        "Inner radius of outboard first wall/blanket coolant channels (stellarator only) [m]":"afwo=0.008     *inner radius of outboard first wall/blanket coolant channels (stellarator only) [m]",  #Fwbs 
        "Switch for first wall coolant (can be different from blanket coolant):":{ 
          "'helium'":"fwcoolant=b'helium'     *'helium'",  #Fwbs 
          "'water'":"fwcoolant=b'water'     *'water'",  #Fwbs 
        },
        "Wall thickness of first wall coolant channels [m]":"fw_wall=0.003     *wall thickness of first wall coolant channels [m]",  #Fwbs 
        "Radius of first wall cooling channels [m]":"afw=0.006     *radius of first wall cooling channels [m]",  #Fwbs 
        "Pitch of first wall cooling channels [m]":"pitch=0.02     *pitch of first wall cooling channels [m]",  #Fwbs 
        "Inlet temperature of first wall coolant [K]":"fwinlet=573     *inlet temperature of first wall coolant [K]",  #Fwbs 
        "Outlet temperature of first wall coolant [K]":"fwoutlet=823     *outlet temperature of first wall coolant [K]",  #Fwbs 
        "First wall coolant pressure [Pa] (secondary_cycle>1)":"fwpressure=15500000     *first wall coolant pressure [Pa] (secondary_cycle>1)",  #Fwbs 
        "Peak first wall temperature [K]":"tpeak=873     *peak first wall temperature [K]",  #Fwbs 
        "First wall channel roughness epsilon [m]":"roughness=0.000001     *first wall channel roughness epsilon [m]",  #Fwbs 
        "Length of a single first wall channel (all in parallel) [m] (iteration variable 114, useful for constraint equation 39)":"fw_channel_length=4     *Length of a single first wall channel (all in parallel) [m] (iteration variable 114, useful for constraint equation 39)",  #Fwbs 
        "Peaking factor for first wall heat loads. (Applied separately to inboard and outboard loads.)":"peaking_factor=1     *peaking factor for first wall heat loads. (Applied separately to inboard and outboard loads.)",  #Fwbs 
        "Blanket coolant pressure [Pa] (secondary_cycle>1)":"blpressure=15500000     *blanket coolant pressure [Pa] (secondary_cycle>1)",  #Fwbs 
        "Inlet temperature of blanket coolant [K] (secondary_cycle>1)":"inlet_temp=573     *inlet temperature of blanket coolant [K] (secondary_cycle>1)",  #Fwbs 
        
        "Outlet temperature of blanket coolant [K] (secondary_cycle>1)":"outlet_temp=823     *Outlet temperature of blanket coolant [K] (secondary_cycle>1)",  #Fwbs 
        "Blanket coolant pressure [Pa] (stellarator only)":"coolp=15500000     *blanket coolant pressure [Pa] (stellarator only)",  #Fwbs 
        "Number of outboard blanket modules in poloidal direction (secondary_cycle>1)":"nblktmodpo=8     *number of outboard blanket modules in poloidal direction (secondary_cycle>1)",  #Fwbs 
        "Number of inboard blanket modules in poloidal direction (secondary_cycle>1)":"nblktmodpi=7     *number of inboard blanket modules in poloidal direction (secondary_cycle>1)",  #Fwbs 
        "Number of outboard blanket modules in toroidal direction (secondary_cycle>1)":"nblktmodto=48     *number of outboard blanket modules in toroidal direction (secondary_cycle>1)",  #Fwbs 
        "Number of inboard blanket modules in toroidal direction (secondary_cycle>1)":"nblktmodti=32     *number of inboard blanket modules in toroidal direction (secondary_cycle>1)",  #Fwbs 
        "Maximum temperature of first wall material [K] (secondary_cycle>1)":"tfwmatmax=823     *maximum temperature of first wall material [K] (secondary_cycle>1)",  #Fwbs 
        "Thermal conductivity of first wall material at 293 K (W/m/K) (Temperature dependence is as for unirradiated Eurofer)":"fw_th_conductivity=28.34     *thermal conductivity of first wall material at 293 K (W/m/K) (Temperature dependence is as for unirradiated Eurofer)",  #Fwbs 
        "Area coverage factor for vacuum vessel volume":"fvoldw=1.74     *area coverage factor for vacuum vessel volume",  #Fwbs 
        "Area coverage factor for inboard shield volume":"fvolsi=1     *area coverage factor for inboard shield volume",  #Fwbs 
        "Area coverage factor for outboard shield volume":"fvolso=0.64     *area coverage factor for outboard shield volume",  #Fwbs 
        "First wall coolant fraction (calculated if lpulse=1 or ipowerflow=1)":"fwclfr=0.15     *first wall coolant fraction (calculated if lpulse=1 or ipowerflow=1)",  #Fwbs 
        "Radiation power incident on the divertor (MW)":"praddiv=     *Radiation power incident on the divertor (MW)",  #Fwbs 
        "Radiation power incident on the first wall (MW)":"pradfw=     *Radiation power incident on the first wall (MW)",  #Fwbs 
        "Radiation power incident on the heating and current drive system (MW)":"pradhcd=     *Radiation power incident on the heating and current drive system (MW)",  #Fwbs 
        "Radiation power lost through holes (eventually hits shield) (MW) Only used for stellarator":"pradloss=     *Radiation power lost through holes (eventually hits shield) (MW) Only used for stellarator",  #Fwbs 
        "Nuclear heating in the TF coil (MW)":"ptfnuc=     *nuclear heating in the TF coil (MW)",  #Fwbs 
        "Nuclear heating in the TF coil (MW/m3) (blktmodel>0)":"ptfnucpm3=     *nuclear heating in the TF coil (MW/m3) (blktmodel>0)",  #Fwbs 
        "Cryostat radius [m]":"rdewex=     *cryostat radius [m]",  #Fwbs 
        "Cryostat height [m]":"zdewex=     *cryostat height [m]",  #Fwbs 
        "Radial distance between outer edge of largest (ipfloc=3) PF coil (or stellarator modular coil) and cryostat [m]":"rpf2dewar=0.5     *radial distance between outer edge of largest (ipfloc=3) PF coil (or stellarator modular coil) and cryostat [m]",  #Fwbs 
        "Cryostat volume [m^3]":"vdewex=     *cryostat volume [m^3]",  #Fwbs 
        "Vacuum vessel volume [m^3]":"vdewin=     *vacuum vessel volume [m^3]",  #Fwbs 
        "Coolant void fraction in shield":"vfshld=0.25     *coolant void fraction in shield",  #Fwbs 
        "Volume of blanket [m^3]":"volblkt=     *volume of blanket [m^3]",  #Fwbs 
        "Volume of inboard blanket [m^3]":"volblkti=     *volume of inboard blanket [m^3]",  #Fwbs 
        "Volume of outboard blanket [m^3]":"volblkto=     *volume of outboard blanket [m^3]",  #Fwbs 
        "Volume of shield [m^3]":"volshld=     *volume of shield [m^3]",  #Fwbs 
        "Mass of shield [kg]":"whtshld=     *mass of shield [kg]",  #Fwbs 
        "Mass of the penetration shield [kg]":"wpenshld=     *mass of the penetration shield [kg]",  #Fwbs 
        "Mass of inboard shield [kg]":"wtshldi=     *mass of inboard shield [kg]",  #Fwbs 
        "Mass of outboard shield [kg]":"wtshldo=     *mass of outboard shield [kg]",  #Fwbs 
        "Switch to use REFPROP routines (stellarator only)":"irefprop=1     *Switch to use REFPROP routines (stellarator only)",  #Fwbs 
        "Lithium fraction of blanket by volume (stellarator only)":"fblli=     *lithium fraction of blanket by volume (stellarator only)",  #Fwbs 
        "Lithium oxide fraction of blanket by volume (stellarator only)":"fblli2o=0.08     *lithium oxide fraction of blanket by volume (stellarator only)",  #Fwbs 
        "Lithium lead fraction of blanket by volume (stellarator only)":"fbllipb=0.68     *lithium lead fraction of blanket by volume (stellarator only)",  #Fwbs 
        "Vanadium fraction of blanket by volume (stellarator only)":"fblvd=     *vanadium fraction of blanket by volume (stellarator only)",  #Fwbs 
        "Mass of blanket - Li_2O part [kg]":"wtblli2o=     *mass of blanket - Li_2O part [kg]",  #Fwbs 
        "Mass of blanket - Li-Pb part [kg]":"wtbllipb=     *mass of blanket - Li-Pb part [kg]",  #Fwbs 
        "Mass of blanket - vanadium part [kg]":"whtblvd=     *mass of blanket - vanadium part [kg]",  #Fwbs 
        "Mass of blanket - lithium part [kg]":"whtblli=     *mass of blanket - lithium part [kg]",  #Fwbs 
        "Coolant void fraction in blanket.":"vfblkt=0.25     *coolant void fraction in blanket.",  #Fwbs 
        "Switch for blanket/tritium breeding model (see iblanket):":{
          "=0 original simple model":"blktmodel=0     *=0 original simple model",  #Fwbs 
          "=1 KIT model based on a helium-cooled pebble-bed blanket (HCPB) reference design":"blktmodel=1     *=1 KIT model based on a helium-cooled pebble-bed blanket (HCPB) reference design",  #Fwbs 
        }, 
        "Neutron power deposition decay length of blanket structural material [m] (stellarators only)":"declblkt=0.075     *neutron power deposition decay length of blanket structural material [m] (stellarators only)",  #Fwbs 
        "Neutron power deposition decay length of first wall structural material [m] (stellarators only)":"declfw=0.075     *neutron power deposition decay length of first wall structural material [m] (stellarators only)",  #Fwbs 
        "Neutron power deposition decay length of shield structural material [m] (stellarators only)":"declshld=0.075     *neutron power deposition decay length of shield structural material [m] (stellarators only)",  #Fwbs 
        "Switch for blanket type:":{
          "=3 Default":"blkttype=3     *",  #Fwbs 
          "=1 WCLL;":"blkttype=1     *=1 WCLL;",  #Fwbs 
          "=2 HCLL":"blkttype=2     *=2 HCLL",  #Fwbs 
          "=3 HCPB":"blkttype=3     *=3 HCPB",  #Fwbs 
        },
        "Isentropic efficiency of FW and blanket coolant pumps":"etaiso=0.85     *isentropic efficiency of FW and blanket coolant pumps",  #Fwbs 
        
        "Electrical efficiency of primary coolant pumps":"etahtp=0.95     *electrical efficiency of primary coolant pumps",  #Fwbs 
        "Switch for whether the FW and BB are on the same pump system. ":"ipump=     *Switch for whether the FW and BB are on the same pump system. ",  #Fwbs 
        "Switch for Liquid Metal Breeder Material - =0 PbLi - =1 Li":"i_bb_liq=     *Switch for Liquid Metal Breeder Material - =0 PbLi - =1 Li",  #Fwbs 
        "Switch to specify whether breeding blanket is single-cooled or dual-coolant.":{
        "=0 Single coolant used for FW and Blanket (H2O or He). Solid Breeder":"icooldual=0     *Single coolant used for FW and Blanket (H2O or He). Solid Breeder",
        "=1 Single coolant used for FW and Blanket (H2O or He). Liquid metal breeder circulted for tritium extraction":"icooldual=1     *Single coolant used for FW and Blanket (H2O or He). Liquid metal breeder circulted for tritium extraction.",
        "=2 Dual coolant: primary coolant (H2O or He) for FW and blanket structure; secondary coolant is self-cooled liquid metal breeder.":"icooldual=2         *Dual coolant: primary coolant (H2O or He) for FW and blanket structure; secondary coolant is self-cooled liquid metal breeder.",  #Fwbs 
        },
        "Switch for Flow Channel Insert (FCI) type if liquid metal breeder blanket. - =0 ":"ifci=     *Switch for Flow Channel Insert (FCI) type if liquid metal breeder blanket. - =0 ",  #Fwbs 
        "Switch for Multi Module Segment (MMS) or Single Modle Segment (SMS) - =0 MMS - =1 SMS":"ims=     *Switch for Multi Module Segment (MMS) or Single Modle Segment (SMS) - =0 MMS - =1 SMS",  #Fwbs 
        "Number of liquid metal breeder recirculations per day, for use with icooldual=1":"n_liq_recirc=10     *Number of liquid metal breeder recirculations per day, for use with icooldual=1",  #Fwbs 
        "Radial fraction of BZ liquid channels":"r_f_liq_ib=0.5     *Radial fraction of BZ liquid channels",  #Fwbs 
        "Radial fraction of BZ liquid channels":"r_f_liq_ob=0.5     *Radial fraction of BZ liquid channels",  #Fwbs 
        "Toroidal fraction of BZ liquid channels":"w_f_liq_ib=0.5     *Toroidal fraction of BZ liquid channels",  #Fwbs 
        "Toroidal fraction of BZ liquid channels":"w_f_liq_ob=0.5     *Toroidal fraction of BZ liquid channels",  #Fwbs 
        "FCI material density":"den_ceramic=3210     *FCI material density",  #Fwbs 
        "Liquid metal coolant/breeder wall thickness thin conductor or FCI [m]":"th_wall_secondary=0.0125     *Liquid metal coolant/breeder wall thickness thin conductor or FCI [m]",  #Fwbs 
        "Liquid metal coolant/breeder thin conductor or FCI wall conductance [A V^-1 m^-1]":"bz_channel_conduct_liq=833000     *Liquid metal coolant/breeder thin conductor or FCI wall conductance [A V^-1 m^-1]",  #Fwbs 
        "Toroidal width of the rectangular cooling channel [m] for long poloidal sections of blanket breeding zone":"a_bz_liq=0.2     *Toroidal width of the rectangular cooling channel [m] for long poloidal sections of blanket breeding zone",  #Fwbs 
        "Radial width of the rectangular cooling channel [m] for long poloidal sections of blanket breeding zone":"b_bz_liq=0.2     *Radial width of the rectangular cooling channel [m] for long poloidal sections of blanket breeding zone",  #Fwbs 
        "Number of poloidal sections in a liquid metal breeder/coolant channel for module/segment":"nopol=2     *Number of poloidal sections in a liquid metal breeder/coolant channel for module/segment",  #Fwbs 
        "Number of Liquid metal breeder/coolant channels per module/segment":"nopipes=4     *Number of Liquid metal breeder/coolant channels per module/segment",  #Fwbs 
        "Liquid metal breeder/coolant density [kg m^-3]":"den_liq=9500     *Liquid metal breeder/coolant density [kg m^-3]",  #Fwbs 
        "Liquid metal":"wht_liq=     *Liquid metal",  #Fwbs 
        "Liquid metal":"wht_liq_ib=     *Liquid metal",  #Fwbs 
        "Liquid metal":"wht_liq_ob=     *Liquid metal",  #Fwbs 
        "Liquid metal breeder/coolant specific heat [J kg^-1 K^-1]":"specific_heat_liq=190     *Liquid metal breeder/coolant specific heat [J kg^-1 K^-1]",  #Fwbs 
        "Liquid metal breeder/coolant thermal conductivity [W m^-1 K^-1]":"thermal_conductivity_liq=30     *Liquid metal breeder/coolant thermal conductivity [W m^-1 K^-1]",  #Fwbs 
        "Liquid metal breeder/coolant dynamic viscosity [Pa s]":"dynamic_viscosity_liq=     *Liquid metal breeder/coolant dynamic viscosity [Pa s]",  #Fwbs 
        "Liquid metal breeder/coolant electrical conductivity [Ohm m]":"electrical_conductivity_liq=     *Liquid metal breeder/coolant electrical conductivity [Ohm m]",  #Fwbs 
        "Hartmann number":"hartmann_liq=     *Hartmann number",  #Fwbs 
        "Toroidal Magnetic feild strength for IB/OB blanket [T]":"b_mag_blkt=[5. 5.]     *Toroidal Magnetic feild strength for IB/OB blanket [T]",  #Fwbs 
        "Isentropic efficiency of blanket liquid breeder/coolant pumps":"etaiso_liq=0.85     *Isentropic efficiency of blanket liquid breeder/coolant pumps",  #Fwbs 
        "Blanket liquid metal breeder/coolant pressure [Pa]":"blpressure_liq=1700000     *blanket liquid metal breeder/coolant pressure [Pa]",  #Fwbs 
        "Inlet (scan var 68) and Outlet (scan var 69) temperature of the liquid breeder/coolant [K]":"inlet_temp_liq=570     *Inlet (scan var 68) and Outlet (scan var 69) temperature of the liquid breeder/coolant [K]",  #Fwbs 
        "Inlet (scan var 68) and Outlet (scan var 69) temperature of the liquid breeder/coolant [K]":"outlet_temp_liq=720     *Inlet (scan var 68) and Outlet (scan var 69) temperature of the liquid breeder/coolant [K]",  #Fwbs 
        "Density of the FW primary coolant":"rhof_fw=     *Density of the FW primary coolant",  #Fwbs 
        "Viscosity of the FW primary coolant":"visc_fw=     *Viscosity of the FW primary coolant",  #Fwbs 
        "Density of the blanket primary coolant":"rhof_bl=     *Density of the blanket primary coolant",  #Fwbs 
        "Viscosity of the blanket primary coolant":"visc_bl=     *Viscosity of the blanket primary coolant",  #Fwbs 
        "Spesific heat for FW and blanket primary coolant(s)":"cp_fw=     *Spesific heat for FW and blanket primary coolant(s)",  #Fwbs 
        "Spesific heat for FW and blanket primary coolant(s)":"cv_fw=     *Spesific heat for FW and blanket primary coolant(s)",  #Fwbs 
        "Spesific heat for FW and blanket primary coolant(s)":"cp_bl=     *Spesific heat for FW and blanket primary coolant(s)",  #Fwbs 
        "Spesific heat for FW and blanket primary coolant(s)":"cv_bl=     *Spesific heat for FW and blanket primary coolant(s)",  #Fwbs 
        "For a dual-coolant blanket, fraction of BZ power cooled by primary coolant":"f_nuc_pow_bz_struct=0.34     *For a dual-coolant blanket, fraction of BZ power cooled by primary coolant",  #Fwbs 
        "For a dual-coolant blanket, fraction of BZ self-cooled power (secondary coolant)":"f_nuc_pow_bz_liq=0.66     *For a dual-coolant blanket, fraction of BZ self-cooled power (secondary coolant)",  #Fwbs 
        "For a dual-coolant blanket, ratio of FW/Blanket nuclear power as fraction of total":"pnuc_fw_ratio_dcll=0.14     *For a dual-coolant blanket, ratio of FW/Blanket nuclear power as fraction of total",  #Fwbs 
        "For a dual-coolant blanket, ratio of FW/Blanket nuclear power as fraction of total":"pnuc_blkt_ratio_dcll=0.86     *For a dual-coolant blanket, ratio of FW/Blanket nuclear power as fraction of total",  #Fwbs 
        "Number of radial and poloidal sections that make up the total primary coolant flow length in a blanket module (IB and OB)":"bzfllengi_n_rad=4     *Number of radial and poloidal sections that make up the total primary coolant flow length in a blanket module (IB and OB)",  #Fwbs 
        "Number of radial and poloidal sections that make up the total primary coolant flow length in a blanket module (IB and OB)":"bzfllengi_n_pol=2     *Number of radial and poloidal sections that make up the total primary coolant flow length in a blanket module (IB and OB)",  #Fwbs 
        "Number of radial and poloidal sections that make up the total primary coolant flow length in a blanket module (IB and OB)":"bzfllengo_n_rad=4     *Number of radial and poloidal sections that make up the total primary coolant flow length in a blanket module (IB and OB)",  #Fwbs 
        "Number of radial and poloidal sections that make up the total primary coolant flow length in a blanket module (IB and OB)":"bzfllengo_n_pol=2     *Number of radial and poloidal sections that make up the total primary coolant flow length in a blanket module (IB and OB)",  #Fwbs 
        "Number of radial and poloidal sections that make up the total secondary coolant/breeder flow length in a blanket module (IB and OB)":"bzfllengi_n_rad_liq=2     *Number of radial and poloidal sections that make up the total secondary coolant/breeder flow length in a blanket module (IB and OB)",  #Fwbs 
        "Number of radial and poloidal sections that make up the total secondary coolant/breeder flow length in a blanket module (IB and OB)":"bzfllengi_n_pol_liq=2     *Number of radial and poloidal sections that make up the total secondary coolant/breeder flow length in a blanket module (IB and OB)",  #Fwbs 
        "Number of radial and poloidal sections that make up the total secondary coolant/breeder flow length in a blanket module (IB and OB)":"bzfllengo_n_rad_liq=2     *Number of radial and poloidal sections that make up the total secondary coolant/breeder flow length in a blanket module (IB and OB)",  #Fwbs 
        "Number of radial and poloidal sections that make up the total secondary coolant/breeder flow length in a blanket module (IB and OB)":"bzfllengo_n_pol_liq=2     *Number of radial and poloidal sections that make up the total secondary coolant/breeder flow length in a blanket module (IB and OB)",  #Fwbs 

    }
    create_checkboxes("Select Fwbs Values", Fwbs_values, 'Fwbs')

#Heat Transport Variables
def Heat_transport_variables():
    """Display a list of checkboxes for the user to select Heat Transport, with a scrollbar."""
    Heat_transport_values = {
         "Base plant electric load (W)":"baseel=5000000     *base plant electric load (W)",  #Heat Transport
        "Cryogenic plant power (MW)":"crypmw=     *cryogenic plant power (MW)",  #Heat Transport
        "Maximum cryogenic plant power (MW) Constraint equation icc = 87 Scan variable nwseep = 56":"crypmw_max=50     *Maximum cryogenic plant power (MW) Constraint equation icc = 87 Scan variable nwseep = 56",  #Heat Transport
        "F-value for maximum cryogenic plant power Iteration variable ixc = 164 Constraint equation icc = 87":"f_crypmw=1     *f-value for maximum cryogenic plant power Iteration variable ixc = 164 Constraint equation icc = 87",  #Heat Transport
        "AC to resistive power conversion for TF coils":"etatf=0.9     *AC to resistive power conversion for TF coils",  #Heat Transport
        "Thermal to electric conversion efficiency if secondary_cycle=2; otherwise calculated.":"etath=0.35     *thermal to electric conversion efficiency if secondary_cycle=2; otherwise calculated.",  #Heat Transport
        "Electrical efficiency of liquid coolant":"etath_liq=0.35     *electrical efficiency of liquid coolant",  #Heat Transport
        "Facility heat removal (MW)":"fachtmw=     *facility heat removal (MW)",  #Heat Transport
        "Total baseline power required at all times (MW)":"fcsht=     *total baseline power required at all times (MW)",  #Heat Transport
        "Scaled fraction of gross power to balance-of-plant":"fgrosbop=     *scaled fraction of gross power to balance-of-plant",  #Heat Transport
        "Power to mgf (motor-generator flywheel) units (MW) (ignored if iscenr=2)":"fmgdmw=     *power to mgf (motor-generator flywheel) units (MW) (ignored if iscenr=2)",  #Heat Transport
        "Fraction of total blanket thermal power required to drive the blanket coolant pumps (default assumes water coolant) (secondary_cycle=0)":"fpumpblkt=0.005     *fraction of total blanket thermal power required to drive the blanket coolant pumps (default assumes water coolant) (secondary_cycle=0)",  #Heat Transport
        "Fraction of total divertor thermal power required to drive the divertor coolant pumps (default assumes water coolant)":"fpumpdiv=0.005     *fraction of total divertor thermal power required to drive the divertor coolant pumps (default assumes water coolant)",  #Heat Transport
        "Fraction of total first wall thermal power required to drive the FW coolant pumps (default assumes water coolant) (secondary_cycle=0)":"fpumpfw=0.005     *fraction of total first wall thermal power required to drive the FW coolant pumps (default assumes water coolant) (secondary_cycle=0)",  #Heat Transport
        "Fraction of total shield thermal power required to drive the shield coolant pumps (default assumes water coolant)":"fpumpshld=0.005     *fraction of total shield thermal power required to drive the shield coolant pumps (default assumes water coolant)",  #Heat Transport
        "Minimum total electrical power for primary coolant pumps (MW) (NOT RECOMMENDED)":"htpmw_min=-     *Minimum total electrical power for primary coolant pumps (MW) (NOT RECOMMENDED)",  #Heat Transport
        "Heat removal at cryogenic temperature tmpcry (W)":"helpow=-     *Heat removal at cryogenic temperature tmpcry (W)",  #Heat Transport
        "Heat removal at cryogenic temperature tcoolin (W)":"helpow_cryal=-     *Heat removal at cryogenic temperature tcoolin (W)",  #Heat Transport
        "Heat transport system electrical pump power (MW)":"htpmw=-     *heat transport system electrical pump power (MW)",  #Heat Transport
        "Blanket primary coolant mechanical pumping power (MW)":"htpmw_blkt=-     *blanket primary coolant mechanical pumping power (MW)",  #Heat Transport
        "Blanket secondary coolant mechanical pumping power (MW)":"htpmw_blkt_liq=-     *blanket secondary coolant mechanical pumping power (MW)",  #Heat Transport
        "Blanket primary + secondary coolant mechanical pumping power (MW)":"htpmw_blkt_tot=-     *blanket primary + secondary coolant mechanical pumping power (MW)",  #Heat Transport
        "Divertor coolant mechanical pumping power (MW)":"htpmw_div=-     *divertor coolant mechanical pumping power (MW)",  #Heat Transport
        "First wall coolant mechanical pumping power (MW)":"htpmw_fw=-     *first wall coolant mechanical pumping power (MW)",  #Heat Transport
        "Shield and vacuum vessel coolant mechanical pumping power (MW)":"htpmw_shld=-     *shield and vacuum vessel coolant mechanical pumping power (MW)",  #Heat Transport
        "Waste power lost from primary coolant pumps (MW)":"htpsecmw=-     *Waste power lost from primary coolant pumps (MW)",  #Heat Transport
        
        "Switch for power flow model:":{
          "=1 Default":"htpmw_fw=1     *",  #Heat Transport
          "=0 pre-2014 version":"ipowerflow=0     *=0 pre-2014 version",  #Heat Transport
          "=1 comprehensive 2014 model":"ipowerflow=1     *=1 comprehensive 2014 model",  #Heat Transport
        },
        "Switch for shield thermal power destiny:":{
          "=1 Default":"iprimshld=1     *",  #Heat Transport 
          "=0 does not contribute to energy generation cycle":"iprimshld=1     *=0 does not contribute to energy generation cycle",  #Heat Transport
          "=1 contributes to energy generation cycle":"iprimshld=1     *=1 contributes to energy generation cycle",  #Heat Transport
        },
        "Number of primary heat exchangers":"nphx=     *number of primary heat exchangers",  #Heat Transport
        "Total pulsed power system load (MW)":"pacpmw=     *total pulsed power system load (MW)",  #Heat Transport
        "Peak MVA requirement":"peakmva=     *peak MVA requirement",  #Heat Transport
        "Heat removal from first wall/divertor (MW)":"pfwdiv=     *heat removal from first wall/divertor (MW)",  #Heat Transport
        "Gross electric power (MW)":"pgrossmw=     *gross electric power (MW)",  #Heat Transport
        "Power dissipated in heating and current drive system (MW)":"pinjht=     *power dissipated in heating and current drive system (MW)",  #Heat Transport
        "Maximum injector power during pulse (heating and ramp-up/down phase) (MW)":"pinjmax=120     *maximum injector power during pulse (heating and ramp-up/down phase) (MW)",  #Heat Transport
        "Injector wall plug power (MW)":"pinjwp=     *injector wall plug power (MW)",  #Heat Transport
        "Secondary injector wall plug power (MW)":"pinjwpfix=     *secondary injector wall plug power (MW)",  #Heat Transport
        "Net electric power (MW)":"pnetelmw=     *net electric power (MW)",  #Heat Transport
        "Recirculating electric power (MW)":"precircmw=     *recirculating electric power (MW)",  #Heat Transport
        "Total thermal power removed from fusion core (MW)":"priheat=     *total thermal power removed from fusion core (MW)",  #Heat Transport
        "Low-grade heat lost in divertor (MW)":"psecdiv=     *Low-grade heat lost in divertor (MW)",  #Heat Transport
        "Low-grade heat lost into HCD apparatus (MW)":"psechcd=     *Low-grade heat lost into HCD apparatus (MW)",  #Heat Transport
        "Low-grade heat (MW)":"psechtmw=     *Low-grade heat (MW)",  #Heat Transport
        "Low-grade heat (VV + lost)(MW)":"pseclossmw=     *Low-grade heat (VV + lost)(MW)",  #Heat Transport
        "Low-grade heat deposited in shield (MW)":"psecshld=     *Low-grade heat deposited in shield (MW)",  #Heat Transport
        "High-grade heat useful for electric production (MW)":"pthermmw=     *High-grade heat useful for electric production (MW)",  #Heat Transport
        "Base AC power requirement per unit floor area (W/m2)":"pwpm2=150     *base AC power requirement per unit floor area (W/m2)",  #Heat Transport
        "Total steady state TF coil AC power demand (MW)":"tfacpd=     *total steady state TF coil AC power demand (MW)",  #Heat Transport
        "Estimate of total low voltage power (MW)":"tlvpmw=     *estimate of total low voltage power (MW)",  #Heat Transport
        "Power required for tritium processing (MW)":"trithtmw=15     *power required for tritium processing (MW)",  #Heat Transport
        "Coolant temperature at turbine inlet (K) (secondary_cycle = 3,4)":"tturb=     *coolant temperature at turbine inlet (K) (secondary_cycle = 3,4)",  #Heat Transport
        "Vacuum pump power (MW)":"vachtmw=0.5     *vacuum pump power (MW)",  #Heat Transport

    }
    create_checkboxes("Select Heat Transport Values", Heat_transport_values, 'Heat_transport')

#Impurity Radiation Variables
def Impurity_Radiation_variables():
    """Display a list of checkboxes for the user to select Impurity Radiation, with a scrollbar."""
    Impurity_Radiation_values = {
        "Coreradius /0.6/ : normalised radius defining the 'core' region":"coreradius=0.6     *coreradius /0.6/ : normalised radius defining the 'core' region",  #Impurity Radiation
        "Coreradiationfraction /1.0/ : fraction of radiation from 'core' region that is subtracted from the loss power":"coreradiationfraction=1     *coreradiationfraction /1.0/ : fraction of radiation from 'core' region that is subtracted from the loss power",  #Impurity Radiation

    }
    create_checkboxes("Select Impurity Radiation", Impurity_Radiation_values, 'IR')

#Numerics Variables
def Numerics():
    """Display a list of checkboxes for the user to select Numerics Variables, with a scrollbar."""
    Numerics_values = {
        "Ioptimz /1/ : code operation switch:":"ioptimz=1     *ioptimz /1/ : code operation switch:",  #Numerics
        "Epsfcn /1.0e-3/ : finite difference step length for HYBRD/VMCON derivatives":"epsfcn=0.001     *epsfcn /1.0e-3/ : finite difference step length for HYBRD/VMCON derivatives",  #Numerics
        "Epsvmc /1.0e-6/ : error tolerance for VMCON":"epsvmc=0.000001     *epsvmc /1.0e-6/ : error tolerance for VMCON",  #Numerics
        "Factor /0.1/ : used in HYBRD for first step size":"factor=0.1     *factor /0.1/ : used in HYBRD for first step size",  #Numerics
        "Ftol /1.0e-4/ : error tolerance for HYBRD":"ftol=0.0001     *ftol /1.0e-4/ : error tolerance for HYBRD",  #Numerics

    }
    create_checkboxes("Select Numerics Values", Numerics_values, 'Numerics')

#CS/Pf coil Variables
def CS_pfcoil_variables():
    """Display a list of checkboxes for the user to select CS_pfcoil, with a scrollbar."""
    CS_pfcoil_values = {
        "Maximum number of groups of PF coils":"ngrpmx=10     *maximum number of groups of PF coils",  #cs/pf coil
        "Maximum number of PF coils in a given group":"nclsmx=2     *maximum number of PF coils in a given group",  #cs/pf coil
        "Maximum number of points across the midplane of the plasma at which the field from the PF coils is fixed":"nptsmx=32     *maximum number of points across the midplane of the plasma at which the field from the PF coils is fixed",  #cs/pf coil
        "Maximum number of fixed current PF coils":"nfixmx=64     *maximum number of fixed current PF coils",  #cs/pf coil
        "Maximum total number of coils across all groups":"ngc=ngrpmx*nclsmx     *maximum total number of coils across all groups",  #cs/pf coil
        "New variable to include 2 additional circuits: plasma and central solenoid":"ngc2=ngc+2     *new variable to include 2 additional circuits: plasma and central solenoid",  #cs/pf coil
        "Smoothing parameter used in PF coil current calculation at the beginning of pulse (BoP)":"alfapf=5.00E-10     *smoothing parameter used in PF coil current calculation at the beginning of pulse (BoP)",  #cs/pf coil
        "Allowable hoop stress in Central Solenoid structural material (Pa)":"alstroh=400000000     *allowable hoop stress in Central Solenoid structural material (Pa)",  #cs/pf coil
        "Switch for CS stress calculation:":{
          "=0 Hoop stress only":"i_os_stress=0     *=0 Hoop stress only",  #cs/pf coil
          "=1 Hoop + Axial stress":"i_os_stress=1     *=1 Hoop + Axial stress",  #cs/pf coil
        },
        "Central solenoid vertical cross-sectional area (m2)":"areaoh=     *Central solenoid vertical cross-sectional area (m2)",  #cs/pf coil
        "Central solenoid (OH) trun cross-sectional area (m2)":"a_oh_turn=     *Central solenoid (OH) trun cross-sectional area (m2)",  #cs/pf coil
        "Central solenoid conductor+void area with area of steel subtracted (m2)":"awpoh=     *central solenoid conductor+void area with area of steel subtracted (m2)",  #cs/pf coil
        "Maximum field in central solenoid at end of flat-top (EoF) (T)":"bmaxoh=     *maximum field in central solenoid at end of flat-top (EoF) (T)",  #cs/pf coil
        "Maximum field in central solenoid at beginning of pulse (T)":"bmaxoh0=     *maximum field in central solenoid at beginning of pulse (T)",  #cs/pf coil
        "Peak field at coil i (T)":"bpf=     *peak field at coil i (T)",  #cs/pf coil
        "PF group current array, flux-swing cancellation current (MA) Input if i_pf_current=0, computed otherwise":"ccl0_ma=     *PF group current array, flux-swing cancellation current (MA) Input if i_pf_current=0, computed otherwise",  #cs/pf coil
        "PF group current array, equilibrium current (MA) Input if i_pf_current=0, computed otherwise":"ccls_ma=     *PF group current array, equilibrium current (MA) Input if i_pf_current=0, computed otherwise",  #cs/pf coil
        "Central solenoid overall current density at beginning of pulse (A/m2)":"cohbop=     *Central solenoid overall current density at beginning of pulse (A/m2)",  #cs/pf coil
        "Central solenoid overall current density at end of flat-top (A/m2) (iteration variable 37) (sweep variable 62)":"coheof=18500000     *Central solenoid overall current density at end of flat-top (A/m2) (iteration variable 37) (sweep variable 62)",  #cs/pf coil
        "Current per turn in coil i at time j (A)":"cpt=     *current per turn in coil i at time j (A)",  #cs/pf coil
        "Peak current per turn input for PF coil i (A)":"cptdin=[40000. 40000. 40000. 40000. 40000. 40000. 40000. 40000. 40000. 40000. 40000. 40000. 40000. 40000. 40000. 40000. 40000. 40000. 40000. 40000. 40000. 40000.]     *peak current per turn input for PF coil i (A)",  #cs/pf coil
        "PF coil current array, at beginning of pulse (MA) Indexed by coil number, not group number":"curpfb=     *PF coil current array, at beginning of pulse (MA) Indexed by coil number, not group number",  #cs/pf coil
        "PF coil current array, at flat top (MA) Indexed by coil number, not group number":"curpff=     *PF coil current array, at flat top (MA) Indexed by coil number, not group number",  #cs/pf coil
        "PF coil current array, at end of pulse (MA) Indexed by coil number, not group number":"curpfs=     *PF coil current array, at end of pulse (MA) Indexed by coil number, not group number",  #cs/pf coil
        "Efficiency of transfer of PF stored energy into or out of storage.":"etapsu=0.9     *Efficiency of transfer of PF stored energy into or out of storage.",  #cs/pf coil
        "Ratio of central solenoid overall current density at beginning of flat-top / end of flat-top":"fcohbof=     *ratio of central solenoid overall current density at beginning of flat-top / end of flat-top",  #cs/pf coil
        "Ratio of central solenoid overall current density at beginning of pulse / end of flat-top (iteration variable 41)":"fcohbop=0.9     *ratio of central solenoid overall current density at beginning of pulse / end of flat-top (iteration variable 41)",  #cs/pf coil
        "Copper fraction of strand in central solenoid":"fcuohsu=0.7     *copper fraction of strand in central solenoid",  #cs/pf coil
        "Copper fraction of cable conductor (PF coils)":"fcupfsu=0.69     *copper fraction of cable conductor (PF coils)",  #cs/pf coil
        "F-value for constraint equation 51":"fvssu=1     *F-value for constraint equation 51",  #cs/pf coil
        
        "Switch for location of PF coil group i:":{
          "Default":"ipfloc=[2 2 3 0 0 0 0 0 0 0]     *Switch for location of PF coil group i:",  #cs/pf coil
          "=1 PF coil on top of central solenoid (flux ramp only)":"ipfloc=1     *=1 PF coil on top of central solenoid (flux ramp only)",  #cs/pf coil
          "=2 PF coil on top of TF coil (flux ramp only)":"ipfloc=2     *=2 PF coil on top of TF coil (flux ramp only)",  #cs/pf coil
          "=3 PF coil outside of TF coil (equilibrium coil)":"ipfloc=3     *=3 PF coil outside of TF coil (equilibrium coil)",  #cs/pf coil
          "=4 PF coil, general location (equilibrium coil)":"ipfloc=4     *=4 PF coil, general location (equilibrium coil)",  #cs/pf coil
        },
        "Switch for PF & CS coil conductor type:":{
          "=0 superconducting PF coils":"ipfres=0     *=0 superconducting PF coils",  #cs/pf coil
          "=1 resistive PF coils":"ipfres=1     *=1 resistive PF coils",  #cs/pf coil
        },
        "Total sum of I x turns x radius for all PF coils and CS (Am)":"itr_sum=     *total sum of I x turns x radius for all PF coils and CS (Am)",  #cs/pf coil
        
        "Switch for superconductor material in central solenoid:":{
          "=1 Default ":"isumatoh=1     *switch for superconductor material in central solenoid",  #cs/pf coil
          "=1 ITER Nb3Sn critical surface model with standard ITER parameters":"isumatoh=1     *=1 ITER Nb3Sn critical surface model with standard ITER parameters",  #cs/pf coil
          "=2 Bi-2212 high temperature superconductor (range of validity T < 20K, adjusted field b < 104 T, B > 6 T)":"isumatoh=2     *=2 Bi-2212 high temperature superconductor (range of validity T < 20K, adjusted field b < 104 T, B > 6 T)",  #cs/pf coil
          "=3 NbTi":"isumatoh=3     *=3 NbTi",  #cs/pf coil
          "=4 ITER Nb3Sn model with user-specified parameters":"isumatoh=4     *=4 ITER Nb3Sn model with user-specified parameters",  #cs/pf coil
          "=5 WST Nb3Sn parameterisation":"isumatoh=5     *=5 WST Nb3Sn parameterisation",  #cs/pf coil
          "=6 REBCO HTS tape in CroCo strand":"isumatoh=6     *=6 REBCO HTS tape in CroCo strand",  #cs/pf coil
          "=7 Durham Ginzburg-Landau critical surface model for Nb-Ti":"isumatoh=7     *=7 Durham Ginzburg-Landau critical surface model for Nb-Ti",  #cs/pf coil
          "=8 Durham Ginzburg-Landau critical surface model for REBCO":"isumatoh=8     *=8 Durham Ginzburg-Landau critical surface model for REBCO",  #cs/pf coil
          "=9 Hazelton experimental data + Zhai conceptual model for REBCO":"isumatoh=9     *=9 Hazelton experimental data + Zhai conceptual model for REBCO",  #cs/pf coil
        },
        "Switch for superconductor material in PF coils:":{
          "=1 Default":"isumatpf=1     *switch for superconductor material in PF coils",  #cs/pf coil
          "=1 ITER Nb3Sn critical surface model with standard ITER parameters":"isumatpf=1     *=1 ITER Nb3Sn critical surface model with standard ITER parameters",  #cs/pf coil
          "=2 Bi-2212 high temperature superconductor (range of validity T < 20K, adjusted field b < 104 T, B > 6 T)":"isumatpf=2     *=2 Bi-2212 high temperature superconductor (range of validity T < 20K, adjusted field b < 104 T, B > 6 T)",  #cs/pf coil
          "=3 NbTi":"isumatpf=3     *=3 NbTi",  #cs/pf coil
          "=4 ITER Nb3Sn model with user-specified parameters":"isumatpf=4     *=4 ITER Nb3Sn model with user-specified parameters",  #cs/pf coil
          "=5 WST Nb3Sn parameterisation":"isumatpf=5     *=5 WST Nb3Sn parameterisation",  #cs/pf coil
          "=6 REBCO HTS tape in CroCo strand":"isumatpf=6     *=6 REBCO HTS tape in CroCo strand",  #cs/pf coil
          "=7 Durham Ginzburg-Landau critical surface model for Nb-Ti":"isumatpf=7     *=7 Durham Ginzburg-Landau critical surface model for Nb-Ti",  #cs/pf coil
          "=8 Durham Ginzburg-Landau critical surface model for REBCO":"isumatpf=8     *=8 Durham Ginzburg-Landau critical surface model for REBCO",  #cs/pf coil
          "=9 Hazelton experimental data + Zhai conceptual model for REBCO":"isumatpf=9     *=9 Hazelton experimental data + Zhai conceptual model for REBCO",  #cs/pf coil
        },
        "Switch for controlling the current of the PF coils:":{
          "=1 Default ":"i_pf_current=1     *Switch for controlling the current of the PF coils",  #cs/pf coil
          "=0 Input via the variables curpfb, curpff, curpfs":"i_pf_current=0     *=0 Input via the variables curpfb, curpff, curpfs",  #cs/pf coil
          "=1 SVD targets zero field across midplane (flux swing coils) and the correct vertical field at the plasma center (equilibrium coils)":"i_pf_current=1     *=1 SVD targets zero field across midplane (flux swing coils) and the correct vertical field at the plasma center (equilibrium coils)",  #cs/pf coil
        },
        "Switch for the placement of Location 3 (outboard) PF coils when the TF coils are superconducting (i_tf_sup = 1)":{
        
          "=0 (Default) Outboard PF coils follow TF shape in an ellipsoidal winding surface":"i_sup_pf_shape=0     *=0 (Default) Outboard PF coils follow TF shape in an ellipsoidal winding surface",  #cs/pf coil
          "=1 Outboard PF coils all have same radius, cylindrical winding surface":"i_sup_pf_shape=1     *=1 Outboard PF coils all have same radius, cylindrical winding surface",  #cs/pf coil
        },
        "Central solenoid superconductor critical current density (A/m2) at beginning-of-pulse":"jscoh_bop=     *central solenoid superconductor critical current density (A/m2) at beginning-of-pulse",  #cs/pf coil
        "Central solenoid superconductor critical current density (A/m2) at end-of-flattop":"jscoh_eof=     *central solenoid superconductor critical current density (A/m2) at end-of-flattop",  #cs/pf coil
        "Central solenoid strand critical current density (A/m2) at beginning-of-pulse":"jstrandoh_bop=     *central solenoid strand critical current density (A/m2) at beginning-of-pulse",  #cs/pf coil
        "Central solenoid strand critical current density (A/m2) at end-of-flattop":"jstrandoh_eof=     *central solenoid strand critical current density (A/m2) at end-of-flattop",  #cs/pf coil
        "Number of PF circuits (including central solenoid and plasma)":"ncirt=     *number of PF circuits (including central solenoid and plasma)",  #cs/pf coil
        "Number of PF coils in group j":"ncls=[1 1 2 0 0 0 0 0 0 0 0 0]     *number of PF coils in group j",  #cs/pf coil
        "Number of filaments the top and bottom of the central solenoid should be broken into during scaling (5 - 10 is good)":"nfxfh=7     *number of filaments the top and bottom of the central solenoid should be broken into during scaling (5 - 10 is good)",  #cs/pf coil
        "Number of groups of PF coils. Symmetric coil pairs should all be in the same group":"ngrp=3     *number of groups of PF coils. Symmetric coil pairs should all be in the same group",  #cs/pf coil
        "Number of PF coils (excluding the central solenoid) + 1":"nohc=     *number of PF coils (excluding the central solenoid) + 1",  #cs/pf coil
        "Central solenoid height / TF coil internal height":"ohhghf=0.71     *Central solenoid height / TF coil internal height",  #cs/pf coil
        "Central solenoid steel fraction (iteration variable 122)":"oh_steel_frac=0.5     *central solenoid steel fraction (iteration variable 122)",  #cs/pf coil
        "Steel case thickness for PF coil i (m)":"pfcaseth=     *steel case thickness for PF coil i (m)",  #cs/pf coil
        "PF coil resistivity (if ipfres=1) (Ohm-m)":"pfclres=0.000000025    *PF coil resistivity (if ipfres=1) (Ohm-m)",  #cs/pf coil
        "Mass of heaviest PF coil (tonnes)":"pfmmax=     *mass of heaviest PF coil (tonnes)",  #cs/pf coil
        "Radius of largest PF coil (m)":"pfrmax=     *radius of largest PF coil (m)",  #cs/pf coil
        "Total mean wall plug power dissipated in PFC and CS power supplies (MW) (issue #713)":"pfwpmw=     *Total mean wall plug power dissipated in PFC and CS power supplies (MW) (issue #713)",  #cs/pf coil
        "Central solenoid resistive power during flattop (W)":"powohres=     *central solenoid resistive power during flattop (W)",  #cs/pf coil
        "Total PF coil resistive losses during flattop (W)":"powpfres=     *total PF coil resistive losses during flattop (W)",  #cs/pf coil
        "Inner radius of coil i (m)":"ra=     *inner radius of coil i (m)",  #cs/pf coil
        "Outer radius of coil i (m)":"rb=     *outer radius of coil i (m)",  #cs/pf coil
        "Peak current in coil i (MA-turns)":"ric=     *peak current in coil i (MA-turns)",  #cs/pf coil
        "Average winding pack current density of PF coil i (A/m2) at time of peak current in that coil (calculated for ipfloc=1 coils)":"rjconpf=[30000000. 30000000. 30000000. 30000000. 30000000. 30000000. 30000000. 30000000. 30000000. 30000000. 30000000. 30000000. 30000000. 30000000. 30000000. 30000000. 30000000. 30000000. 30000000. 30000000. 30000000. 30000000.]     *average winding pack current density of PF coil i (A/m2) at time of peak current in that coil (calculated for ipfloc=1 coils)",  #cs/pf coil
        "Allowable central solenoid current density at end of flat-top (A/m2)":"rjohc=     *allowable central solenoid current density at end of flat-top (A/m2)",  #cs/pf coil
        "Allowable central solenoid current density at beginning of pulse (A/m2)":"rjohc0=     *allowable central solenoid current density at beginning of pulse (A/m2)",  #cs/pf coil
        "Allowable winding pack current density of PF coil i (A/m2)":"rjpfalw=     *allowable winding pack current density of PF coil i (A/m2)",  #cs/pf coil
        "Radius to the centre of the central solenoid (m)":"rohc=     *radius to the centre of the central solenoid (m)",  #cs/pf coil
        "Radial distance (m) from outboard TF coil leg to centre of ipfloc=3 PF coils":"routr=1.5     *radial distance (m) from outboard TF coil leg to centre of ipfloc=3 PF coils",  #cs/pf coil
        "Radius of PF coil i (m)":"rpf=     *radius of PF coil i (m)",  #cs/pf coil
        "Offset (m) of radial position of ipfloc=1 PF coils from being directly above the central solenoid":"rpf1=     *offset (m) of radial position of ipfloc=1 PF coils from being directly above the central solenoid",  #cs/pf coil
        "Offset (m) of radial position of ipfloc=2 PF coils from being at rmajor (offset = rpf2triangrminor)":"rpf2=-1.63     *offset (m) of radial position of ipfloc=2 PF coils from being at rmajor (offset = rpf2triangrminor)",  #cs/pf coil
        
        "PF coil radial positioning adjuster:":"rref=[7.7.7.7.7.7.7.7.7.7.7]     *PF coil radial positioning adjuster:",  #cs/pf coil
        "Maximum shear stress (Tresca criterion) coils/central solenoid [MPa]":"s_tresca_oh=     *Maximum shear stress (Tresca criterion) coils/central solenoid [MPa]",  #cs/pf coil
        "Maximum permissible tensile stress (MPa) in steel coil cases for superconducting PF coils (ipfres=0)":"sigpfcalw=500     *maximum permissible tensile stress (MPa) in steel coil cases for superconducting PF coils (ipfres=0)",  #cs/pf coil
        "Fraction of JxB hoop force supported by steel case for superconducting PF coils (ipfres=0)":"sigpfcf=0.666     *fraction of JxB hoop force supported by steel case for superconducting PF coils (ipfres=0)",  #cs/pf coil
        "Mutual inductance matrix (H)":"sxlg=     *mutual inductance matrix (H)",  #cs/pf coil
        "Central solenoid temperature margin (K)":"tmargoh=     *Central solenoid temperature margin (K)",  #cs/pf coil
        "Number of turns in PF coil i":"turns=     *number of turns in PF coil i",  #cs/pf coil
        "Winding pack void fraction of PF coil i for coolant":"vf=[0.3 0.3 0.3 0.3 0.3 0.3 0.3 0.3 0.3 0.3 0.3 0.3 0.3 0.3 0.3 0.3 0.3 0.3 0.3 0.3 0.3 0.3]     *winding pack void fraction of PF coil i for coolant",  #cs/pf coil
        "Void fraction of central solenoid conductor for coolant":"vfohc=0.3     *void fraction of central solenoid conductor for coolant",  #cs/pf coil
        "Total flux swing available for burn (Wb)":"vsbn=     *total flux swing available for burn (Wb)",  #cs/pf coil
        "Flux swing from PF coils for burn (Wb)":"vsefbn=     *flux swing from PF coils for burn (Wb)",  #cs/pf coil
        "Flux swing from PF coils for startup (Wb)":"vsefsu=     *flux swing from PF coils for startup (Wb)",  #cs/pf coil
        "Total flux swing from PF coils (Wb)":"vseft=     *total flux swing from PF coils (Wb)",  #cs/pf coil
        "Total flux swing from the central solenoid (Wb)":"vsoh=     *total flux swing from the central solenoid (Wb)",  #cs/pf coil
        "Central solenoid flux swing for burn (Wb)":"vsohbn=     *central solenoid flux swing for burn (Wb)",  #cs/pf coil
        "Central solenoid flux swing for startup (Wb)":"vsohsu=     *central solenoid flux swing for startup (Wb)",  #cs/pf coil
        "Total flux swing for startup (constraint eqn 51 to enforce vssu=vsres+vsind) (Wb)":"vssu=     *total flux swing for startup (constraint eqn 51 to enforce vssu=vsres+vsind) (Wb)",  #cs/pf coil
        "Total flux swing for pulse (Wb)":"vstot=     *total flux swing for pulse (Wb)",  #cs/pf coil
        "Used in current waveform of PF coils/central solenoid":"waves=     *used in current waveform of PF coils/central solenoid",  #cs/pf coil
        "Total mass of the PF coil conductor (kg)":"whtpf=     *total mass of the PF coil conductor (kg)",  #cs/pf coil
        "Total mass of the PF coil structure (kg)":"whtpfs=     *total mass of the PF coil structure (kg)",  #cs/pf coil
        "Conductor mass for PF coil i (kg)":"wtc=     *conductor mass for PF coil i (kg)",  #cs/pf coil
        "Structure mass for PF coil i (kg)":"wts=     *structure mass for PF coil i (kg)",  #cs/pf coil
        "Upper point of PF coil i (m)":"zh=     *upper point of PF coil i (m)",  #cs/pf coil
        "Lower point of PF coil i (m)":"zl=     *lower point of PF coil i (m)",  #cs/pf coil
        "Z (height) location of PF coil i (m)":"zpf=     *z (height) location of PF coil i (m)",  #cs/pf coil
        
        "PF coil vertical positioning adjuster:":"zref=[3.6 1.2 2.5 1. 1. 1. 1. 1. 1. 1. ]     *PF coil vertical positioning adjuster:",  #cs/pf coil
        "Central solenoid max field limit [T]":"bmaxcs_lim=13     *Central solenoid max field limit [T]",  #cs/pf coil
        "F-value for CS mmax field (cons. 79, itvar 149)":"fbmaxcs=1     *F-value for CS mmax field (cons. 79, itvar 149)",  #cs/pf coil
        "Ratio of CS coil turn conduit length to depth":"ld_ratio_cst=3     *Ratio of CS coil turn conduit length to depth",  #cs/pf coil
        "Length of CS of CS coil turn conduit":"l_cond_cst=     *Length of CS of CS coil turn conduit",  #cs/pf coil
        "Depth/width of CS of CS coil turn conduit":"d_cond_cst=     *Depth/width of CS of CS coil turn conduit",  #cs/pf coil
        "Length of CS of CS coil turn conduit length":"r_out_cst=0.003     *Length of CS of CS coil turn conduit length",  #cs/pf coil
        "Length of CS of CS coil turn conduit length":"r_in_cst=     *Length of CS of CS coil turn conduit length",  #cs/pf coil
    }
    create_checkboxes("Select CS/pf Coil", CS_pfcoil_values, 'CS_pf')

#Physics Variables
def Physics():
    """Display a list of checkboxes for the user to select Physics Variables, with a scrollbar."""
    Physics_values = {
        "Current profile index (calculated from q_0, q if iprofile=1)":"alphaj=1     *current profile index (calculated from q_0, q if iprofile=1)",  #Physics
         "Density profile index":"alphan=0.25     *density profile index",  #Physics
         "Temperature profile index":"alphat=0.5     *temperature profile index",  #Physics
         "Aspect ratio (iteration variable 1)":"aspect=2.907     *aspect ratio (iteration variable 1)",  #Physics
         "Multiplier for beam-background fusion calculation":"beamfus0=1     *multiplier for beam-background fusion calculation",  #Physics
         "Total plasma beta (iteration variable 5) (calculated if stellarator)":"beta=0.042     *total plasma beta (iteration variable 5) (calculated if stellarator)",  #Physics
         "Leading coefficient for NB beta fraction":"betbm0=1.5     *leading coefficient for NB beta fraction",  #Physics
         "Toroidal field on axis (T) (iteration variable 2)":"bt=5.68     *toroidal field on axis (T) (iteration variable 2)",  #Physics
         "Coeff. for sawteeth effects on burn V-s requirement":"csawth=1     *coeff. for sawteeth effects on burn V-s requirement",  #Physics
         "Multiplying factor times plasma volume (normally=1)":"cvol=1     *multiplying factor times plasma volume (normally=1)",  #Physics
         "Maximum ratio of conducting wall distance to plasma minor radius for vertical stability (constraint equation 23)":"cwrmax=1.35     *maximum ratio of conducting wall distance to plasma minor radius for vertical stability (constraint equation 23)",  #Physics
         "Electron density (/m3) (iteration variable 6)":"dene=98000000000000000000     *electron density (/m3) (iteration variable 6)",  #Physics
         "Troyon-like coefficient for beta scaling calculated as 4*rli if iprofile=1 (see also gtscale option)":"dnbeta=3.5     *Troyon-like coefficient for beta scaling calculated as 4*rli if iprofile=1 (see also gtscale option)",  #Physics
         "Maximum (eps*beta_poloidal) (constraint equation 6).":"epbetmax=1.38     *maximum (eps*beta_poloidal) (constraint equation 6).",  #Physics
         "Inverse aspect ratio":"eps=0.343997248     *inverse aspect ratio",  #Physics
         "Fraction of alpha power deposited in plasma (Physics of Energetic Ions, p.2489)":"falpha=0.95     *fraction of alpha power deposited in plasma (Physics of Energetic Ions, p.2489)",  #Physics
         "Deuterium fuel fraction":"fdeut=0.5     *deuterium fuel fraction",  #Physics
         "Fraction of power to the lower divertor in double null configuration (i_single_null = 0 only) (default assumes SN)":"ftar=1     *fraction of power to the lower divertor in double null configuration (i_single_null = 0 only) (default assumes SN)",  #Physics
         "Factor to convert plasma surface area to first wall area in neutron wall load calculation (iwalld=1)":"ffwal=0.92     *factor to convert plasma surface area to first wall area in neutron wall load calculation (iwalld=1)",  #Physics
         "Fraction of Greenwald density to set as pedestal-top density. If <0, pedestal-top density set manually using neped (ipedestal==1). (iteration variable 145)":"fgwped=0.85     *fraction of Greenwald density to set as pedestal-top density. If <0, pedestal-top density set manually using neped (ipedestal==1). (iteration variable 145)",  #Physics
         "Fraction of Greenwald density to set as separatrix density. If <0, separatrix density set manually using nesep (ipedestal==1). (iteration variable 152)":"fgwsep=0.5     *fraction of Greenwald density to set as separatrix density. If <0, separatrix density set manually using nesep (ipedestal==1). (iteration variable 152)",  #Physics
         "Zohm elongation scaling adjustment factor (ishape=2, 3)":"fkzohm=1     *Zohm elongation scaling adjustment factor (ishape=2, 3)",  #Physics
         "F-value for Psep >= Plh + Paux (constraint equation 73)":"fplhsep=1     *F-value for Psep >= Plh + Paux (constraint equation 73)",  #Physics
         "F-value for minimum pdivt (constraint equation 80)":"fpdivlim=1     *F-value for minimum pdivt (constraint equation 80)",  #Physics
         "F-value for the constraint ne(0) > ne(ped) (constraint equation 81) (Iteration variable 154)":"fne0=1     *f-value for the constraint ne(0) > ne(ped) (constraint equation 81) (Iteration variable 154)",  #Physics
         "Tritium fuel fraction":"ftrit=0.5     *tritium fuel fraction",  #Physics
         "Fraction of the plasma current produced by non-inductive means (iteration variable 44)":"fvsbrnni=1     *fraction of the plasma current produced by non-inductive means (iteration variable 44)",  #Physics
         "Ejima coefficient for resistive startup V-s formula":"gamma=0.4     *Ejima coefficient for resistive startup V-s formula",  #Physics
         "H factor on energy confinement times, radiation corrected (iteration variable 10).":"hfact=1     *H factor on energy confinement times, radiation corrected (iteration variable 10).",  #Physics
         "Maximum allowed energy confinement time (s)":"taumax=10     *Maximum allowed energy confinement time (s)",  #Physics
         "Switch for bootstrap current scaling":"ibss=3     *switch for bootstrap current scaling",  #Physics
         "Switch for plasma current scaling to use":"icurr=4     *switch for plasma current scaling to use",  #Physics
         "Switch for density limit to enforce (constraint equation 5)":"idensl=7     *switch for density limit to enforce (constraint equation 5)",  #Physics
         "Number of divertors (calculated from i_single_null)":"idivrt=2     *number of divertors (calculated from i_single_null)",  #Physics
         "Switch for fast alpha pressure calculation":"ifalphap=1     *switch for fast alpha pressure calculation",  #Physics
         "Switch for inverse quadrature in L-mode scaling laws 5 and 9:":"iinvqd=1     *switch for inverse quadrature in L-mode scaling laws 5 and 9:",  #Physics
         "Switch for pedestal profiles:":"ipedestal=1     *switch for pedestal profiles:",  #Physics
         "Adjustment factor for EPED scaling to reduce pedestal temperature or pressure to mitigate or prevent ELMs":"eped_sf=1     *Adjustment factor for EPED scaling to reduce pedestal temperature or pressure to mitigate or prevent ELMs",  #Physics
         "Electron density of pedestal [m-3] (`ipedestal==1)":"neped=40000000000000000000     *electron density of pedestal [m-3] (`ipedestal==1)",  #Physics
         "Electron density at separatrix [m-3] (`ipedestal==1)":"nesep=30000000000000000000     *electron density at separatrix [m-3] (`ipedestal==1)",  #Physics
         "Plasma resistivity pre-factor":"plasma_res_factor=1     *plasma resistivity pre-factor",  #Physics
         "r/a of density pedestal (ipedestal==1)":"rhopedn=1     *r/a of density pedestal (ipedestal==1)",  #Physics
         "r/a of temperature pedestal (ipedestal==1)":"rhopedt=1     *r/a of temperature pedestal (ipedestal==1)",  #Physics
         "Temperature profile index beta (`ipedestal==1)":"tbeta=2     *temperature profile index beta (`ipedestal==1)",  #Physics
         "Electron temperature of pedestal (keV) (ipedestal==1, ieped=0, calculated for ieped=1)":"teped=1     *electron temperature of pedestal (keV) (ipedestal==1, ieped=0, calculated for ieped=1)",  #Physics
         "Electron temperature at separatrix (keV) (ipedestal==1) calculated if reinke criterion is used (icc=78)":"tesep=0.1     *electron temperature at separatrix (keV) (ipedestal==1) calculated if reinke criterion is used (icc=78)",  #Physics
         "Switch for current profile consistency:":"iprofile=1     *switch for current profile consistency:",  #Physics
         "Switch for radiation loss term usage in power balance (see User Guide):":"iradloss=1     *switch for radiation loss term usage in power balance (see User Guide):",  #Physics
         "Switch for energy confinement time scaling law (see description in tauscl)":"isc=34     *switch for energy confinement time scaling law (see description in tauscl)",  #Physics
         "Switch for plasma-first wall clearances:":"iscrp=1     *switch for plasma-first wall clearances:",  #Physics
         "Switch for neutron wall load calculation:":"iwalld=1     *switch for neutron wall load calculation:",  #Physics
         "Plasma separatrix elongation (calculated if ishape = 1-5, 7 or 9-10)":"kappa=1.792     *plasma separatrix elongation (calculated if ishape = 1-5, 7 or 9-10)",  #Physics
         "Plasma elongation at 95% surface (calculated if ishape = 0-3, 6, or 8-10)":"kappa95=1.6     *plasma elongation at 95% surface (calculated if ishape = 0-3, 6, or 8-10)",  #Physics
         "Margin to vertical stability":"m_s_limit=0.3     *margin to vertical stability",  #Physics
         "Switch for L-H mode power threshold scaling to use (see pthrmw for list)":"ilhthresh=19     *switch for L-H mode power threshold scaling to use (see pthrmw for list)",  #Physics
         "Safety factor 'near' plasma edge (iteration variable 18) equal to q95 (unless icurr=2 (ST current scaling), in which case q = mean edge safety factor qbar)":"q=3     *safety factor 'near' plasma edge (iteration variable 18) equal to q95 (unless icurr=2 (ST current scaling), in which case q = mean edge safety factor qbar)",  #Physics
         "Safety factor on axis":"q0=1     *safety factor on axis",  #Physics
         "Tauratio /1.0/ : ratio of He and pellet particle confinement times":"tauratio=1     *tauratio /1.0/ : ratio of He and pellet particle confinement times",  #Physics
         "SoL radiation fraction":"rad_fraction_sol=0.8     *SoL radiation fraction",  #Physics
         "Thermal alpha density/electron density (iteration variable 109)":"ralpne=0.1     *thermal alpha density/electron density (iteration variable 109)",  #Physics
         "Plasma normalised internal inductance (calculated from alphaj if iprofile=1)":"rli=0.9     *plasma normalised internal inductance (calculated from alphaj if iprofile=1)",  #Physics
         "Plasma major radius (m) (iteration variable 3)":"rmajor=8.14     *plasma major radius (m) (iteration variable 3)",  #Physics
         "Hot beam density / n_e (iteration variable 7)":"rnbeam=0.005     *hot beam density / n_e (iteration variable 7)",  #Physics
         "Switch for single null / double null plasma:":"i_single_null=1     *switch for single null / double null plasma:",  #Physics
         "Synchrotron wall reflectivity factor":"ssync=0.6     *synchrotron wall reflectivity factor",  #Physics
         "Volume averaged electron temperature (keV) (iteration variable 4)":"te=12.9     *volume averaged electron temperature (keV) (iteration variable 4)",  #Physics
         "Volume averaged ion temperature (keV). N.B. calculated from te if tratio > 0.0":"ti=12.9     *volume averaged ion temperature (keV). N.B. calculated from te if tratio > 0.0",  #Physics
         "Ion temperature / electron temperature(used to calculate ti if tratio > 0.0":"tratio=1     *ion temperature / electron temperature(used to calculate ti if tratio > 0.0",  #Physics
         "Plasma separatrix triangularity (calculated if ishape = 1, 3-5 or 7)":"triang=0.36     *plasma separatrix triangularity (calculated if ishape = 1, 3-5 or 7)",  #Physics
         "Plasma triangularity at 95% surface (calculated if ishape = 0-2, 6, 8 or 9)":"triang95=0.24     *plasma triangularity at 95% surface (calculated if ishape = 0-2, 6, 8 or 9)",  #Physics

    }
    create_checkboxes("Select Physics Values", Physics_values, 'Physics')

#Pulse Variables
def Pulse():
    """Display a list of checkboxes for the user to select Pulse Variables, with a scrollbar."""
    Pulse_values = {
        "first wall bulk coolant temperature (C)":"bctmp=320     *first wall bulk coolant temperature (C)",  # Pulse
        "maximum allowable temperature change in stainless steel thermal storage block (K) (istore=3)":"dtstor=300+H4:I16     *maximum allowable temperature change in stainless steel thermal storage block (K) (istore=3)",  # Pulse
        "Switch for thermal storage method:":"istore=1     *Switch for thermal storage method:",  # Pulse
        "Switch for first wall axial stress model:":"itcycl=1     *Switch for first wall axial stress model:",  # Pulse
    
    }
    create_checkboxes("Select Pulse Values", Pulse_values, 'Pulse')

#Tf Coil Variables
def Tfcoil():
    """Display a list of checkboxes for the user to select Tfcoil, with a scrollbar."""
    Tfcoil_values = {
        "External case area per coil (inboard leg) (m2)":"acasetf=     *external case area per coil (inboard leg) (m2)",   #tfcoil
        "External case area per coil (outboard leg) (m2)":"acasetfo=     *external case area per coil (outboard leg) (m2)",   #tfcoil
        "Area of the cable conduit (m2)":"acndttf=     *area of the cable conduit (m2)",   #tfcoil
        "Winding pack conductor area [m2] Does not include the area of voids and central helium channel":"acond=     *Winding pack conductor area [m2] Does not include the area of voids and central helium channel",   #tfcoil
        "Cable space area (per turn) [m2] Includes the area of voids and central helium channel":"acstf=     *Cable space area (per turn) [m2] Includes the area of voids and central helium channel",   #tfcoil
        "Single turn insulation area (m2)":"insulation_area=     *single turn insulation area (m2)",   #tfcoil
        "Winding pack turn insulation area per coil (m2)":"aiwp=     *winding pack turn insulation area per coil (m2)",   #tfcoil
        "Allowable maximum shear stress (Tresca criterion) in TF coil case (Pa)":"sig_tf_case_max=600000000     *Allowable maximum shear stress (Tresca criterion) in TF coil case (Pa)",   #tfcoil
        "Allowable maximum shear stress (Tresca criterion) in TF coil conduit (Pa)":"sig_tf_wp_max=600000000     *Allowable maximum shear stress (Tresca criterion) in TF coil conduit (Pa)",   #tfcoil
        "Allowable Tresca stress in TF coil structural material (Pa)":"sig_tf_wp_max=600000000     *Allowable Tresca stress in TF coil structural material (Pa)",   #tfcoil
        "Outboard TF leg area (m2)":"arealeg=     *outboard TF leg area (m2)",   #tfcoil
        "Winding pack structure area (m2)":"aswp=     *winding pack structure area (m2)",   #tfcoil
        "Winding pack void (He coolant) area (m2)":"avwp=     *winding pack void (He coolant) area (m2)",   #tfcoil
        "Winding pack He coil area (m2)":"awphec=     *winding pack He coil area (m2)",   #tfcoil
        "Upper critical field (T) for Nb3Sn superconductor at zero temperature and strain (i_tf_sc_mat=4, =bc20m)":"bcritsc=24     *upper critical field (T) for Nb3Sn superconductor at zero temperature and strain (i_tf_sc_mat=4, =bc20m)",   #tfcoil
        "Mean peak field at TF coil (T)":"bmaxtf=     *mean peak field at TF coil (T)",   #tfcoil
        "Peak field at TF conductor with ripple (T)":"bmaxtfrp=     *peak field at TF conductor with ripple (T)",   #tfcoil
        "Case strain":"casestr=     *case strain",   #tfcoil
        "Inboard TF coil case plasma side thickness (m) (calculated for stellarators)":"casthi=     *inboard TF coil case plasma side thickness (m) (calculated for stellarators)",   #tfcoil
        "Inboard TF coil case plasma side thickness as a fraction of tfcth":"casthi_fraction=0.05     *inboard TF coil case plasma side thickness as a fraction of tfcth",   #tfcoil
        "Logical switch to make casthi a fraction of TF coil thickness (casthi_fraction)":"casthi_is_fraction=     *logical switch to make casthi a fraction of TF coil thickness (casthi_fraction)",   #tfcoil
        "Inboard TF coil sidewall case thickness (m) (calculated for stellarators)":"casths=     *inboard TF coil sidewall case thickness (m) (calculated for stellarators)",   #tfcoil
        "Inboard TF coil sidewall case thickness as a fraction of tftort":"casths_fraction=0.06     *inboard TF coil sidewall case thickness as a fraction of tftort",   #tfcoil
        "Logical switch to make casths a fraction of TF coil thickness (casths_fraction)":"tfc_sidewall_is_fraction=     *logical switch to make casths a fraction of TF coil thickness (casths_fraction)",   #tfcoil
        "Conductor (cable + steel conduit) area averaged dimension [m]":"t_conductor=     *Conductor (cable + steel conduit) area averaged dimension [m]",   #tfcoil
        "TF coil turn edge length including turn insulation [m]":"t_turn_tf=     *TF coil turn edge length including turn insulation [m] If the turn is not a square, a squared turn of equivelent size is use to calculated this quantity If the t_turn_tf is non zero, cpttf is calculated",   #tfcoil
        "Boolean switch to activated when the user set the TF coil turn dimensions Not an input":"t_turn_tf_is_input=     *Boolean switch to activated when the user set the TF coil turn dimensions Not an input",   #tfcoil
        "F-value for TF turn edge length constraint If the turn is not a square":"f_t_turn_tf=     *f-value for TF turn edge length constraint If the turn is not a square (i_tf_turns_integer = 1) a squared turn of equivelent size is use for this constraint iteration variable ixc = 175 constraint equation icc = 86",   #tfcoil
        "TF turn edge length including turn insulation upper limit [m]":"t_turn_tf_max=0.05     *TF turn edge length including turn insulation upper limit [m] If the turn is not a square (i_tf_turns_integer = 1) a squared turn of equivelent size is use for this constraint constraint equation icc = 86",   #tfcoil
        "TF coil superconducting cable squared/rounded dimensions [m]":"t_cable_tf=     *TF coil superconducting cable squared/rounded dimensions [m]",   #tfcoil
        "Boolean switch to activated when the user set the TF coil cable dimensions Not an input":"t_cable_tf_is_input=     *Boolean switch to activated when the user set the TF coil cable dimensions Not an input",   #tfcoil
        "Area of space inside conductor (m2)":"acs=     *Area of space inside conductor (m2)",   #tfcoil
        "TF outboard leg current density (A/m2) (resistive coils only)":"cdtfleg=     *TF outboard leg current density (A/m2) (resistive coils only)",   #tfcoil
        "Centering force on inboard leg (per coil) (N/m)":"cforce=     *centering force on inboard leg (per coil) (N/m)",   #tfcoil
        "Length of TF coil inboard leg ('centrepost') (i_tf_sup = 1)":"cplen=     *length of TF coil inboard leg ('centrepost') (i_tf_sup = 1)",   #tfcoil
        "TF coil current per turn (A). (calculated for stellarators) (calculated for integer-turn TF coils i_tf_turns_integer=1) (iteration variable 60)":"cpttf=70000     *TF coil current per turn (A). (calculated for stellarators) (calculated for integer-turn TF coils i_tf_turns_integer=1) (iteration variable 60)",   #tfcoil
        "Max TF coil current per turn [A]. (for stellarators and i_tf_turns_integer=1) (constraint equation 77)":"cpttf_max=90000     *Max TF coil current per turn [A]. (for stellarators and i_tf_turns_integer=1) (constraint equation 77)",   #tfcoil
        "Density of coil case (kg/m3)":"dcase=8000     *density of coil case (kg/m3)",   #tfcoil
        "Density of superconductor type given by i_tf_sc_mat/isumatoh/isumatpf (kg/m3)":"dcond=[6080. 6080. 6070. 6080. 6080. 8500. 6070. 8500. 8500.]     *density of superconductor type given by i_tf_sc_mat/isumatoh/isumatpf (kg/m3)",   #tfcoil
        "Density of conduit + ground-wall insulation (kg/m3)":"dcondins=1800     *density of conduit + ground-wall insulation (kg/m3)",   #tfcoil
        "Diameter of central helium channel in TF winding (m)":"dhecoil=0.005     *diameter of central helium channel in TF winding (m)",   #tfcoil
        "Total stored energy in the toroidal field (GJ)":"estotftgj=     *total stored energy in the toroidal field (GJ)",   #tfcoil
        "Upper critical field of GL_nbti":"b_crit_upper_nbti=14.86     *upper critical field of GL_nbti",   #tfcoil
        "Critical temperature of GL_nbti":"t_crit_nbti=9.04     *critical temperature of GL_nbti",   #tfcoil
        "Maximal (WP averaged) force density in TF coils at 1 point. (MN/m3)":"max_force_density=     *Maximal (WP averaged) force density in TF coils at 1 point. (MN/m3)",   #tfcoil
        "Copper fraction of cable conductor (TF coils) (iteration variable 59)":"fcutfsu=0.69     *copper fraction of cable conductor (TF coils) (iteration variable 59)",   #tfcoil
        "Technology adjustment factor for critical current density fit for isumat.":"fhts=0.5     *technology adjustment factor for critical current density fit for isumat.",   #tfcoil
        "Radial strain in insulator":"insstrain=     *Radial strain in insulator",   #tfcoil
        "Switch for the TF coil stress model ":{
          "Generalized plane strain formulation, Issues #977 and #991, O(n^3)":"i_tf_stress_model=0     *Generalized plane strain formulation, Issues #977 and #991, O(n^3)",
          "Old plane stress model (only for SC)":"i_tf_stress_model=1     *Old plane stress model (only for SC)",
          "Axisymmetric extended plane strain, Issues #1414 and #998, O(n)":"i_tf_stress_model=2     *Axisymmetric extended plane strain, Issues #1414 and #998, O(n)",
        },
        "Switch for TF coil conduit Tresca stress criterion: 0 : Tresca (no adjustment); 1 : Tresca with CEA adjustment factors (radial+2%, vertical+60%)":"i_tf_tresca=     *Switch for TF coil conduit Tresca stress criterion: 0 : Tresca (no adjustment); 1 : Tresca with CEA adjustment factors (radial+2%, vertical+60%)",   #tfcoil
        "Switch for TF WP geometry selection":{
           "Rectangular geometry ":"i_tf_wp_geom=0     *Rectangular geometry",
           "Double rectangular geometry ":"i_tf_wp_geom=1     *Double rectangular geometry",
           "Trapezoidal geometry (constant lateral casing thickness) ":"i_tf_wp_geom=2     *Trapezoidal geometry (constant lateral casing thickness)",
        },
        "Switch for TF case geometry selection 0 : Circular front case (ITER design) 1 : Straight front case":"i_tf_case_geom=     *Switch for TF case geometry selection 0 : Circular front case (ITER design) 1 : Straight front case",   #tfcoil
        "Switch for TF coil integer/non-integer turns: 0 : non-integer turns 1 : integer turns":"i_tf_turns_integer=     *Switch for TF coil integer/non-integer turns: 0 : non-integer turns 1 : integer turns",   #tfcoil
        "Switch for superconductor material in TF coils:":{
           "=1 Default":"i_tf_sc_mat=1     *0",   #tfcoil
           "=1 ITER Nb3Sn critical surface model with standard ITER parameters":"i_tf_sc_mat=1     *=1 ITER Nb3Sn critical surface model with standard ITER parameters",   #tfcoil
           "=2 Bi-2212 high temperature superconductor (range of validity T < 20K, adjusted field b < 104 T, B > 6 T)":"i_tf_sc_mat=2     *=2 Bi-2212 high temperature superconductor (range of validity T < 20K, adjusted field b < 104 T, B > 6 T)",   #tfcoil
           "=3 NbTi":"i_tf_sc_mat=3     *=3 NbTi",   #tfcoil
           "=4 ITER Nb3Sn model with user-specified parameters":"i_tf_sc_mat=4     *=4 ITER Nb3Sn model with user-specified parameters",   #tfcoil
           "=5 WST Nb3Sn parameterisation":"i_tf_sc_mat=5     *=5 WST Nb3Sn parameterisation",   #tfcoil
           "=6 REBCO HTS tape in CroCo strand":"i_tf_sc_mat=6     *=6 REBCO HTS tape in CroCo strand",   #tfcoil
           "=7 Durham Ginzburg-Landau critical surface model for Nb-Ti":"i_tf_sc_mat=7     *=7 Durham Ginzburg-Landau critical surface model for Nb-Ti",   #tfcoil
           "=8 Durham Ginzburg-Landau critical surface model for REBCO":"i_tf_sc_mat=8     *=8 Durham Ginzburg-Landau critical surface model for REBCO",   #tfcoil
           "=9 Hazelton experimental data + Zhai conceptual model for REBCO":"i_tf_sc_mat=9     *=9 Hazelton experimental data + Zhai conceptual model for REBCO",   #tfcoil
        },
        "Switch for TF coil conductor model:":{
          "=1 Default":"i_tf_sup=1     *0",   #tfcoil
          "=0 copper":"i_tf_sup=1     *=0 copper",   #tfcoil
          "=1 superconductor":"i_tf_sup=1     *=1 superconductor",   #tfcoil
          "=2 Cryogenic aluminium":"i_tf_sup=1     *=2 Cryogenic aluminium",   #tfcoil
        },
        "Switch for TF coil toroidal shape:":{
          "=0 Default value : Picture frame coil for TART / PROCESS D-shape for non itart":"i_tf_shape=0     *=0 Default value : Picture frame coil for TART / PROCESS D-shape for non itart",   #tfcoil
          "=1 PROCESS D-shape : parametrise with 2 arcs":"i_tf_shape=1     *=1 PROCESS D-shape : parametrise with 2 arcs",   #tfcoil
          "=2 Picture frame coils":"i_tf_shape=2     *=2 Picture frame coils",   #tfcoil
        },
        "Switch for the behavior of the TF coil conductor elastic axial properties":{
          "=0 Young's modulus is set to zero, and the conductor is not considered in the stress calculation. This corresponds to the case that the conductor is much less stiff than the conduit, or the case that the conductor is prevented (isolated) from taking axial loads.":"i_tf_cond_eyoung_axial=0     *=0 Young's modulus is set to zero, and the conductor is not considered in the stress calculation. This corresponds to the case that the conductor is much less stiff than the conduit, or the case that the conductor is prevented (isolated) from taking axial loads.",   #tfcoil
          "=1 Elastic properties are set by user input, using the variable eyoung_cond_axial":"i_tf_cond_eyoung_axial=1     *=1 Elastic properties are set by user input, using the variable eyoung_cond_axial",   #tfcoil
          "=2 Elastic properties are set to reasonable defaults taking into account the superconducting material i_tf_sc_mat":"i_tf_cond_eyoung_axial=2     *=2 Elastic properties are set to reasonable defaults taking into account the superconducting material i_tf_sc_mat",   #tfcoil
        },
        "Switch for the behavior of the elastic properties of the TF coil conductorin the transverse direction. Only active if i_tf_cond_eyoung_axial == 2":{
          "=1 Default":"i_tf_cond_eyoung_trans=1     *0",   #tfcoil
          "=0 Cable not potted in solder. Transverse Young's modulus set to zero.":"i_tf_cond_eyoung_trans=0     *=0 Cable not potted in solder. Transverse Young's modulus set to zero.",   #tfcoil
          "=1 Cable potted in solder. If i_tf_cond_eyoung_axial == 2, the transverse Young's modulus of the conductor is equal to the axial, which is set to a sensible material-dependent default.":"i_tf_cond_eyoung_trans=1     *=1 Cable potted in solder. If i_tf_cond_eyoung_axial == 2, the transverse Young's modulus of the conductor is equal to the axial, which is set to a sensible material-dependent default.",   #tfcoil
        },
        "Number of pancakes in TF coil. Only used if i_tf_turns_integer=1":"n_pancake=10     *Number of pancakes in TF coil. Only used if i_tf_turns_integer=1",   #tfcoil
        "Number of layers in TF coil. Only used if i_tf_turns_integer=1":"n_layer=20     *Number of layers in TF coil. Only used if i_tf_turns_integer=1",   #tfcoil
        "Size of the arrays per layers storing the radial dependent stress quantities (stresses, strain displacement etc..)":"n_rad_per_layer=100     *Size of the arrays per layers storing the radial dependent stress quantities (stresses, strain displacement etc..)",   #tfcoil
        #i_tf_bucking
        "Switch for TF inboard suport structure design:":"i_tf_bucking=-1     *Switch for TF inboard suport structure design:",   #tfcoil
        "Switch for tf bucking cylinder":{
          "Free standing TF without case/bucking cyliner (only a conductor layer)":"i_tf_bucking=0     *Free standing TF without case/bucking cyliner (only a conductor layer)",
          "Free standing TF with a case/bucking cylinder made of - if copper resistive TF":"i_tf_bucking=1     *Free standing TF with a case/bucking cylinder made of - if copper resistive TF",
          "The TF is in contact with the CS : 'bucked and wedged design' Fast version":"i_tf_bucking=2     *The TF is in contact with the CS : 'bucked and wedged design' Fast version",
          "The TF is in contact with the CS : 'bucked and wedged design' Full version":"i_tf_bucking=3     *The TF is in contact with the CS : 'bucked and wedged design' Full version",
        },
        "Number of layers of different stress properties in the WP. If n_tf_graded_layers > 1, a graded coil is condidered":"C=1     *Number of layers of different stress properties in the WP. If n_tf_graded_layers > 1, a graded coil is condidered",   #tfcoil
        "Number of layers considered for the inboard TF stress calculations set in initial.f90 from i_tf_bucking and n_tf_graded_layers":"n_tf_stress_layers=     *Number of layers considered for the inboard TF stress calculations set in initial.f90 from i_tf_bucking and n_tf_graded_layers",   #tfcoil
        "Maximum number of layers that can be considered in the TF coil composited/smeared stress analysis.":"n_tf_wp_layers=5     *Maximum number of layers that can be considered in the TF coil composited/smeared stress analysis.",   #tfcoil
        "Bussing current density (A/m2)":"jbus=1250000     *bussing current density (A/m2)",   #tfcoil
        "Critical current density for winding pack (A/m2)":"jwdgcrt=     *critical current density for winding pack (A/m2)",   #tfcoil
        "Allowable TF coil winding pack current density, for dump temperature rise protection (A/m2)":"jwdgpro=     *allowable TF coil winding pack current density, for dump temperature rise protection (A/m2)",   #tfcoil
        "Winding pack engineering current density (A/m2)":"jwptf=     *winding pack engineering current density (A/m2)",   #tfcoil
        "Insulator Young's modulus [Pa]. Default value (1.0D8) setup the following values - SC TF, eyoung_ins = 20 Gpa":"eyoung_ins=100000000     *Insulator Young's modulus [Pa]. Default value (1.0D8) setup the following values - SC TF, eyoung_ins = 20 Gpa",   #tfcoil
        "Steel case Young's modulus (Pa) (default value from DDD11-2 v2 2 (2009))":"eyoung_steel=205000000000     *Steel case Young's modulus (Pa) (default value from DDD11-2 v2 2 (2009))",   #tfcoil
        "SC TF coil conductor Young's modulus in the parallel (along the wire/tape) direction [Pa] ":"eyoung_cond_axial=660000000     *SC TF coil conductor Young's modulus in the parallel (along the wire/tape) direction [Pa]",   #tfcoil
        "SC TF coil conductor Young's modulus in the transverse direction [Pa]":"eyoung_cond_trans=     *SC TF coil conductor Young's modulus in the transverse direction [Pa]",   #tfcoil
        "Resistive TF magnets bucking cylinder young modulus (Pa)":"eyoung_res_tf_buck=150000000000     *Resistive TF magnets bucking cylinder young modulus (Pa)",   #tfcoil
        "Copper young modulus. Default value taken from wikipedia":"eyoung_copper=117000000000     *Copper young modulus. Default value taken from wikipedia",   #tfcoil
        "Aluminium young modulus. Default value taken from wikipedia":"eyoung_al=69000000000     *Aluminium young modulus. Default value taken from wikipedia",   #tfcoil
        "Steel Poisson's ratio, Source : https://www.engineeringtoolbox.com/metals-poissons-ratio-d_1268.html":"poisson_steel=0.3     *Steel Poisson's ratio, Source : https://www.engineeringtoolbox.com/metals-poissons-ratio-d_1268.html",   #tfcoil
        "Copper Poisson's ratio. Source : https://www.engineeringtoolbox.com/poissons-ratio-d_1224.html":"poisson_copper=0.35     *Copper Poisson's ratio. Source : https://www.engineeringtoolbox.com/poissons-ratio-d_1224.html",   #tfcoil
        "Aluminium Poisson's ratio. Source : https://www.engineeringtoolbox.com/poissons-ratio-d_1224.html":"poisson_al=0.35     *Aluminium Poisson's ratio. Source : https://www.engineeringtoolbox.com/poissons-ratio-d_1224.html",   #tfcoil
        "Insulation Poisson's ratio. Default: Kapton. Source : DuPont™ Kapton® HN datasheet.":"poisson_ins=0.34     *Insulation Poisson's ratio. Default: Kapton. Source : DuPont™ Kapton® HN datasheet.",   #tfcoil
        "SC TF coil conductor Poisson's ratio in the parallel-transverse direction":"poisson_cond_axial=0.300000012     *SC TF coil conductor Poisson's ratio in the parallel-transverse direction",   #tfcoil
        "SC TF coil conductor Poisson's ratio in the transverse-transverse direction":"poisson_cond_trans=0.300000012     *SC TF coil conductor Poisson's ratio in the transverse-transverse direction",   #tfcoil
        "Radius of maximum TF B-field (m)":"rbmax=     *Radius of maximum TF B-field (m)",   #tfcoil
        "TF coil leg resistance (ohm)":"tflegres=     *TF coil leg resistance (ohm)",   #tfcoil
        "Minimal distance between two toroidal coils. (m)":"toroidalgap=1     *Minimal distance between two toroidal coils. (m)",   #tfcoil
        "F-value for minimum tftort (constraint equation 82)":"ftoroidalgap=1     *F-value for minimum tftort (constraint equation 82)",   #tfcoil
        "Aximum allowable toroidal field ripple amplitude at plasma edge (%)":"ripmax=1     *aximum allowable toroidal field ripple amplitude at plasma edge (%)",   #tfcoil
        "Peak/average toroidal field ripple at plasma edge (%)":"ripple=     *peak/average toroidal field ripple at plasma edge (%)",   #tfcoil
        "Total (summed) current in TF coils (A)":"ritfc=     *total (summed) current in TF coils (A)",   #tfcoil
        "Size of the radial distribution arrays per layers used for stress, strain and displacement distibution":"n_radial_array=50     *Size of the radial distribution arrays per layers used for stress, strain and displacement distibution",   #tfcoil
        "Array refining the radii of the stress calculations arrays":"radial_array=     *Array refining the radii of the stress calculations arrays",   #tfcoil
        "TF Inboard leg radial stress in steel r distribution at mid-plane [Pa]":"sig_tf_r=     *TF Inboard leg radial stress in steel r distribution at mid-plane [Pa]",   #tfcoil
        "TF Inboard leg tangential stress in steel r distribution at mid-plane [Pa]":"sig_tf_t=     *TF Inboard leg tangential stress in steel r distribution at mid-plane [Pa]",   #tfcoil
        "TF coil radial deflection (displacement) radial distribution [m]":"deflect=     *TF coil radial deflection (displacement) radial distribution [m]",   #tfcoil
        "TF Inboard leg vertical tensile stress in steel at mid-plane [Pa]":"sig_tf_z=     *TF Inboard leg vertical tensile stress in steel at mid-plane [Pa]",   #tfcoil
        "TF Inboard leg Von-Mises stress in steel r distribution at mid-plane [Pa]":"sig_tf_vmises=     *TF Inboard leg Von-Mises stress in steel r distribution at mid-plane [Pa]",   #tfcoil
        "TF Inboard leg maximum shear stress (Tresca criterion) in steel r distribution at mid-plane [Pa]":"sig_tf_tresca=     *TF Inboard leg maximum shear stress (Tresca criterion) in steel r distribution at mid-plane [Pa]",   #tfcoil
        "Maximum shear stress (Tresca criterion) in CS structures at CS flux swing [Pa]:":{
          "Maximum shear stress (Tresca criterion) in CS structures at CS flux swing [Pa]:":"sig_tf_cs_bucked=     *Maximum shear stress (Tresca criterion) in CS structures at CS flux swing [Pa]:",   #tfcoil
          "If superconducting CS (ipfres = 0): turn steel conduits stress":"sig_tf_cs_bucked=     *If superconducting CS (ipfres = 0): turn steel conduits stress",   #tfcoil
          "If resistive CS (ipfres = 1): copper conductor stress":"sig_tf_cs_bucked=     *If resistive CS (ipfres = 1): copper conductor stress",   #tfcoil
          "Quantity only computed for bucked and wedged design (i_tf_bucking >= 2) Def : CS Flux swing, instant when the current changes sign in CS (null current)":"sig_tf_cs_bucked=     *Quantity only computed for bucked and wedged design (i_tf_bucking >= 2) Def : CS Flux swing, instant when the current changes sign in CS (null current)",   #tfcoil
          "Maximum shear stress (Tresca criterion) in TF casing steel structures (Pa)":"sig_tf_case=     *Maximum shear stress (Tresca criterion) in TF casing steel structures (Pa)",   #tfcoil
        },
        "Residual manufacturing strain in CS superconductor material":"str_cs_con_res=-0.005     *Residual manufacturing strain in CS superconductor material",   #tfcoil
        "Residual manufacturing strain in PF superconductor material":"str_pf_con_res=-0.005     *Residual manufacturing strain in PF superconductor material",   #tfcoil
        "Residual manufacturing strain in TF superconductor material.":"str_tf_con_res=-0.005     *Residual manufacturing strain in TF superconductor material.",   #tfcoil
        "Axial (vertical) strain in the TF coil winding pack found by self-consistent stress/strain calculation.":"str_wp=     *Axial (vertical) strain in the TF coil winding pack found by self-consistent stress/strain calculation. if i_str_wp == 1, used to compute the critical surface. Otherwise, the input value str_tf_con_res is used.",   #tfcoil
        "Maximum allowed absolute value of the strain in the TF coil (Constraint equation 88)":"str_wp_max=0.007     *Maximum allowed absolute value of the strain in the TF coil (Constraint equation 88)",   #tfcoil
        "Switch for the behavior of the TF strain used to compute the strain-dependent critical surface:":{
          "=1 Default":"i_str_wp=1     *",   #tfcoil   
          "=0 str_tf_con_res is used":"i_str_wp=0     *=0 str_tf_con_res is used",   #tfcoil
          "=1 str_wp is used":"i_str_wp=1     *=1 str_wp is used",   #tfcoil
        },
        "Switch for TF coil quench model (Only applies to REBCO magnet at present, issue #522):":{
          "='exponential' exponential quench with constant discharge resistor":"quench_model=b'exponential     *='exponential' exponential quench with constant discharge resistor",   #tfcoil
          "='linear' quench with constant voltage":"quench_model=b'linear'     *='linear' quench with constant voltage",   #tfcoil
        },
        "Time at which TF quench is detected (s)":"time1=     *Time at which TF quench is detected (s)",   #tfcoil
        "Critical temperature (K) for superconductor at zero field and strain (i_tf_sc_mat=4, =tc0m)":"tcritsc=16     *critical temperature (K) for superconductor at zero field and strain (i_tf_sc_mat=4, =tc0m)",   #tfcoil
        #tdmptf
        "Fast discharge time for TF coil in event of quench (s) (iteration variable 56)":"tdmptf=10     *fast discharge time for TF coil in event of quench (s) (iteration variable 56)",   #tfcoil
        "For REBCO model, meaning depends on quench_model:":"tdmptf=10     *For REBCO model, meaning depends on quench_model:",   #tfcoil
        "Exponential quench : e-folding time (s)`":"tdmptf=10     *exponential quench : e-folding time (s)`",   #tfcoil
        "Linear quench : discharge time (s)":"tdmptf=10     *linear quench : discharge time (s)",   #tfcoil
    
        "Area of inboard midplane TF legs (m2)":"tfareain=     *Area of inboard midplane TF legs (m2)",   #tfcoil
        "TF coil bus length (m)":"tfbusl=     *TF coil bus length (m)",   #tfcoil
        "TF coil bus mass (kg)":"tfbusmas=     *TF coil bus mass (kg)",   #tfcoil
        "Available DC power for charging the TF coils (kW)":"tfckw=     *available DC power for charging the TF coils (kW)",   #tfcoil
        "Peak power per TF power supply (MW)":"tfcmw=     *Peak power per TF power supply (MW)",   #tfcoil
        "Peak resistive TF coil inboard leg power (MW)":"tfcpmw=     *Peak resistive TF coil inboard leg power (MW)",   #tfcoil
        "TF joints resistive power losses (MW)":"tfjtsmw=     *TF joints resistive power losses (MW)",   #tfcoil
        "Surface area of toroidal shells covering TF coils (m2)":"tfcryoarea=     *surface area of toroidal shells covering TF coils (m2)",   #tfcoil
        "TF coil half-width - inner bore (m)":"tficrn=     *TF coil half-width - inner bore (m)",   #tfcoil
        "TF coil inductance (H)":"tfind=     *TF coil inductance (H)",   #tfcoil
        "TF coil WP insertion gap (m)":"tfinsgap=0.01     *TF coil WP insertion gap (m)",   #tfcoil
        "TF coil outboard leg resistive power (MW)":"tflegmw=     *TF coil outboard leg resistive power (MW)",   #tfcoil
        "TF coil inboard leg resistivity [Ohm-m]. If itart=0, this variable is the average resistivity over the whole magnet":"rhocp=     *TF coil inboard leg resistivity [Ohm-m]. If itart=0, this variable is the average resistivity over the whole magnet",   #tfcoil
        "Resistivity of a TF coil leg (Ohm-m)":"rhotfleg=     *Resistivity of a TF coil leg (Ohm-m)",   #tfcoil
        "Resistivity of a TF coil bus (Ohm-m). Default value takes the same res as the leg one":"rhotfbus=-1     *Resistivity of a TF coil bus (Ohm-m). Default value takes the same res as the leg one",   #tfcoil
        "Centrepost resistivity enhancement factor. For itart=0, this factor is used for the whole magnet":"frhocp=1     *Centrepost resistivity enhancement factor. For itart=0, this factor is used for the whole magnet",   #tfcoil
        "Ouboard legs resistivity enhancement factor. Only used for itart=1.":"frholeg=1     *Ouboard legs resistivity enhancement factor. Only used for itart=1.",   #tfcoil
        "Switch for CP demoutable joints type":{
          "Clampled joints":"i_cp_joints=0     *Clampled joints",
          "Sliding joints Default value (-1)":"i_cp_joints=1     *Sliding joints Default value (-1)", 
        },
        "TF joints surfacic resistivity [ohm.m]. Feldmetal joints assumed.":"rho_tf_joints=2.50E-10     *TF joints surfacic resistivity [ohm.m]. Feldmetal joints assumed.",   #tfcoil
        "Number of contact per turn":"n_tf_joints_contact=6     *Number of contact per turn",   #tfcoil
        "Number of joints Ex: n_tf_joints = 2 for top and bottom CP joints":"n_tf_joints=4     *Number of joints Ex: n_tf_joints = 2 for top and bottom CP joints",   #tfcoil
        "TF sliding joints contact pad width [m]":"th_joint_contact=0.03     *TF sliding joints contact pad width [m]",   #tfcoil
        "Calculated TF joints resistive power losses [W]":"pres_joints=     *Calculated TF joints resistive power losses [W]",   #tfcoil
        "TF coil circumference (m)":"tfleng=     *TF coil circumference (m)",   #tfcoil
        "TF cryoplant efficiency (compared to pefect Carnot cycle). Using -1 set the default value depending on magnet technology:":{
          "=-1 Default":"eff_tf_cryo=-1     *0",   #tfcoil
          "i_tf_sup = 1 : SC magnet, eff_tf_cryo = 0.13 (ITER design)":"eff_tf_cryo=0.13     *i_tf_sup = 1 : SC magnet, eff_tf_cryo = 0.13 (ITER design)",   #tfcoil
          "i_tf_sup = 2 : Cryo-aluminium, eff_tf_cryo = 0.4":"eff_tf_cryo=-1     *i_tf_sup =0.4 : Cryo-aluminium, eff_tf_cryo = 0.4",   #tfcoil
        },
        "Number of TF coils (default = 50 for stellarators). Number of TF coils outer legs for ST":"n_tf=16     *Number of TF coils (default = 50 for stellarators). Number of TF coils outer legs for ST",   #tfcoil
        "TF coil half-width - outer bore (m)":"tfocrn=     *TF coil half-width - outer bore (m)",   #tfcoil
        "Area of the inboard TF coil legs (m2)":"tfsai=     *area of the inboard TF coil legs (m2)",   #tfcoil
        "Area of the outboard TF coil legs (m2)":"tfsao=     *area of the outboard TF coil legs (m2)",   #tfcoil
        "Peak helium coolant temperature in TF coils and PF coils (K)":"tftmp=4.5     *peak helium coolant temperature in TF coils and PF coils (K)",   #tfcoil
        "TF coil toroidal thickness (m)":"tftort=1     *TF coil toroidal thickness (m)",   #tfcoil
        "Conduit insulation thickness (m)":"thicndut=0.0008     *conduit insulation thickness (m)",   #tfcoil
        "Additional insulation thickness between layers (m)":"layer_ins=     *Additional insulation thickness between layers (m)",   #tfcoil
        "Inboard TF coil case outer (non-plasma side) thickness (m) (iteration variable 57) (calculated for stellarators)":"thkcas=0.3     *inboard TF coil case outer (non-plasma side) thickness (m) (iteration variable 57) (calculated for stellarators)",   #tfcoil
        "Radial thickness of winding pack (m) (iteration variable 140) (issue #514)":"dr_tf_wp=     *radial thickness of winding pack (m) (iteration variable 140) (issue #514)",   #tfcoil
        "TF coil conduit case thickness (m) (iteration variable 58)":"thwcndut=0.008     *TF coil conduit case thickness (m) (iteration variable 58)",   #tfcoil
        "Thickness of the ground insulation layer surrounding (m) - Superconductor TF (i_tf_sup == 1)":"tinstf=0.018     *Thickness of the ground insulation layer surrounding (m) - Superconductor TF (i_tf_sup == 1)",   #tfcoil
        "Minimum allowable temperature margin : TF coils (K)":"tmargmin_tf=     *minimum allowable temperature margin : TF coils (K)",   #tfcoil
        "Minimum allowable temperature margin : CS (K)":"tmargmin_cs=     *minimum allowable temperature margin : CS (K)",   #tfcoil
        "Minimum allowable temperature margin : TFC AND CS (K)":"tmargmin=     *minimum allowable temperature margin : TFC AND CS (K)",   #tfcoil
        "Temperature margin (K)":"temp_margin=     *temperature margin (K)",   #tfcoil
        "TF coil temperature margin (K)":"tmargtf=     *TF coil temperature margin (K)",   #tfcoil
        "Maximum temp rise during a quench for protection (K)":"tmaxpro=150     *maximum temp rise during a quench for protection (K)",   #tfcoil
        "CroCo strand: maximum permitted temp during a quench (K)":"tmax_croco=200     *CroCo strand: maximum permitted temp during a quench (K)",   #tfcoil
        "CroCo strand: Actual temp reached during a quench (K)":"croco_quench_temperature=     *CroCo strand: Actual temp reached during a quench (K)",   #tfcoil
        "Coil temperature for cryogenic plant power calculation (K)":"tmpcry=4.5     *coil temperature for cryogenic plant power calculation (K)",   #tfcoil
        "Number of turns per TF coil":"n_tf_turn=     *number of turns per TF coil",   #tfcoil
        "Max voltage across TF coil during quench (kV) (iteration variable 52)":"vdalw=20     *max voltage across TF coil during quench (kV) (iteration variable 52)",   #tfcoil
        "Vertical tension on inboard leg/coil (N)":"vforce=     *vertical tension on inboard leg/coil (N)",   #tfcoil
        "Fraction of the total vertical force taken by the TF inboard leg tension Not used for resistive itart=1 (sliding joints)":"f_vforce_inboard=0.5     *Fraction of the total vertical force taken by the TF inboard leg tension Not used for resistive itart=1 (sliding joints)",   #tfcoil
        "Vertical tension on outboard leg/coil (N)":"vforce_outboard=     *Vertical tension on outboard leg/coil (N)",   #tfcoil
        "Coolant fraction of TFC 'cable' (i_tf_sup=1), or of TFC leg (i_tf_ssup=0)":"vftf=0.4     *coolant fraction of TFC 'cable' (i_tf_sup=1), or of TFC leg (i_tf_ssup=0)",   #tfcoil
        "Volume of each TF coil outboard leg (m3)":"voltfleg=     *volume of each TF coil outboard leg (m3)",   #tfcoil
        "TF coil voltage for resistive coil including bus (kV)":"vtfkv=     *TF coil voltage for resistive coil including bus (kV)",   #tfcoil
        "Voltage across a TF coil during quench (kV)":"vtfskv=     *voltage across a TF coil during quench (kV)",   #tfcoil
        "Mass per coil of external case (kg)":"whtcas=     *mass per coil of external case (kg)",   #tfcoil
        "TF coil conductor mass per coil (kg/coil). For itart=1, coil is return limb plus centrepost/n_tf":"whtcon=     *TF coil conductor mass per coil (kg/coil). For itart=1, coil is return limb plus centrepost/n_tf",   #tfcoil
        "Copper mass in TF coil conductor (kg/coil). For itart=1, coil is return limb plus centrepost/n_tf":"whtconcu=     *copper mass in TF coil conductor (kg/coil). For itart=1, coil is return limb plus centrepost/n_tf",   #tfcoil
        "Aluminium mass in TF coil conductor (kg/coil). For itart=1, coil is return limb plus centrepost/n_tf":"whtconal=     *Aluminium mass in TF coil conductor (kg/coil). For itart=1, coil is return limb plus centrepost/n_tf",   #tfcoil
        "Conduit insulation mass in TF coil conductor (kg/coil)":"whtconin=     *conduit insulation mass in TF coil conductor (kg/coil)",   #tfcoil
        "Superconductor mass in TF coil cable (kg/coil)":"whtconsc=     *superconductor mass in TF coil cable (kg/coil)",   #tfcoil
        "Steel conduit mass in TF coil conductor (kg/coil)":"whtconsh=     *steel conduit mass in TF coil conductor (kg/coil)",   #tfcoil
        "Mass of ground-wall insulation layer per coil (kg/coil)":"whtgw=     *mass of ground-wall insulation layer per coil (kg/coil)",   #tfcoil
        "Total mass of the TF coils (kg)":"whttf=     *total mass of the TF coils (kg)",   #tfcoil
        "Width of first step of winding pack (m)":"wwp1=     *width of first step of winding pack (m)",   #tfcoil
        "Width of second step of winding pack (m)":"wwp2=     *width of second step of winding pack (m)",   #tfcoil
        "Angle of arc i (rad)":"dthet=     *angle of arc i (rad)",   #tfcoil
        "Radius of arc i (m)":"radctf=     *radius of arc i (m)",   #tfcoil
        "X location of arc point i on surface (m)":"xarc=     *x location of arc point i on surface (m)",   #tfcoil
        "X location of arc centre i (m)":"xctfc=     *x location of arc centre i (m)",   #tfcoil
        "Y location of arc point i on surface (m)":"yarc=     *y location of arc point i on surface (m)",   #tfcoil
        "Y location of arc centre i (m)":"yctfc=     *y location of arc centre i (m)",   #tfcoil
        "Horizontal radius of inside edge of TF coil (m)":"tfa=     *Horizontal radius of inside edge of TF coil (m)",   #tfcoil
        "Vertical radius of inside edge of TF coil (m)":"tfb=     *Vertical radius of inside edge of TF coil (m)",   #tfcoil
        "Centrepost taper maximum radius adjustment (m)":"drtop=     *centrepost taper maximum radius adjustment (m)",   #tfcoil
        "Centrepost taper height adjustment (m)":"dztop=     *centrepost taper height adjustment (m)",   #tfcoil
        "Centrepost coolant pump efficiency":"etapump=0.8     *centrepost coolant pump efficiency",   #tfcoil
        "Coolant fraction of TF coil inboard legs (iteration variable 23)":"fcoolcp=0.3     *coolant fraction of TF coil inboard legs (iteration variable 23)",   #tfcoil
        "Coolant fraction of TF coil outboard legs":"fcoolleg=0.2     *coolant fraction of TF coil outboard legs",   #tfcoil
        "Centrepost cooling area toroidal cross-section (constant over the whole CP)":"a_cp_cool=     *Centrepost cooling area toroidal cross-section (constant over the whole CP)",   #tfcoil
        "Number of centrepost coolant tubes":"ncool=     *number of centrepost coolant tubes",   #tfcoil
        "Centrepost coolant pump power (W)":"ppump=     *centrepost coolant pump power (W)",   #tfcoil
        "Resistive power in the centrepost (itart=1) [W]. If itart=0, this variable is the ressitive power on the whole magnet":"prescp=     *resistive power in the centrepost (itart=1) [W]. If itart=0, this variable is the ressitive power on the whole magnet",   #tfcoil
        "Summed resistive power in the TF coil legs [W]. Remain 0 if itart=0.":"presleg=     *Summed resistive power in the TF coil legs [W]. Remain 0 if itart=0.",   #tfcoil
        "Maximum peak centrepost temperature (K) (constraint equation 44)":"ptempalw=473.15     *maximum peak centrepost temperature (K) (constraint equation 44)",   #tfcoil
        "Average radius of coolant channel (m) (iteration variable 69)":"rcool=0.005     *average radius of coolant channel (m) (iteration variable 69)",   #tfcoil
        "Centrepost coolant inlet temperature (K)":"tcoolin=313.15     *centrepost coolant inlet temperature (K)",   #tfcoil
        "Inlet / outlet TF coil coolant temperature rise (K)":"dtiocool=     *inlet / outlet TF coil coolant temperature rise (K)",   #tfcoil
        "Computed centrepost average temperature (K) (for consistency)":"tcpav2=     *Computed centrepost average temperature (K) (for consistency)",   #tfcoil
        "Peak centrepost temperature (K)":"tcpmax=     *peak centrepost temperature (K)",   #tfcoil
        "Inlet centrepost coolant flow speed at midplane (m/s) (iteration variable 70)":"vcool=20     *inlet centrepost coolant flow speed at midplane (m/s) (iteration variable 70)",   #tfcoil
        "Exact conductor volume in the centrepost (m3)":"vol_cond_cp=     *Exact conductor volume in the centrepost (m3)",   #tfcoil
        "Mass of TF coil inboard legs (kg)":"whtcp=     *mass of TF coil inboard legs (kg)",   #tfcoil
        "Mass of the TF coil legs (kg)":"whttflgs=     *mass of the TF coil legs (kg)",   #tfcoil
        "Cryo cooling requirement at helium temp 4.5K (kW)":"cryo_cool_req=     *Cryo cooling requirement at helium temp 4.5K (kW)",   #tfcoil
        "The angle of the outboard arc forming the TF coil current center line [deg]":"theta1_coil=45     *The angle of the outboard arc forming the TF coil current center line [deg]",   #tfcoil
        "The angle of the outboard arc forming the Vacuum Vessel current center line [deg]":"theta1_vv=1     *The angle of the outboard arc forming the Vacuum Vessel current center line [deg]",   #tfcoil
        "The allowable peak maximum shear stress in the vacuum vessel due to quench and fast discharge of the TF coils [Pa]":"max_vv_stress=143000000     *The allowable peak maximum shear stress in the vacuum vessel due to quench and fast discharge of the TF coils [Pa]",   #tfcoil

    }
    create_checkboxes("Select Tfcoil Value", Tfcoil_values, 'Tf_coil')

def new2_simple_ribbon():
    """Create a simple ribbon-like interface with buttons wrapping to new lines."""
    if hasattr(root, 'ribbon_frame') and root.ribbon_frame.winfo_exists():
        root.ribbon_frame.destroy()
    else:
        if hasattr(root, 'ribbon_frame'):
            root.ribbon_frame.destroy()

        # Ribbon Frame
        ribbon_frame = tk.Frame(root, bg="pink", padx=5, pady=5)
        ribbon_frame.pack(fill=tk.X, side=tk.TOP, before=text_box)

        # Left arrow button for scrolling left
        left_arrow = tk.Button(ribbon_frame, text="<", command=lambda: canvas.xview_scroll(-1, 'units'), padx=5, pady=2)
        left_arrow.pack(side=tk.LEFT, fill=tk.Y)

        # Scrollable Canvas to hold the ribbon content
        canvas = tk.Canvas(ribbon_frame, bg="lightgray", height=50)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Buttons Container inside the canvas
        button_container = tk.Frame(canvas, bg="lightgray")
        canvas.create_window((0, 0), window=button_container, anchor="nw")

        # Right arrow button for scrolling right
        right_arrow = tk.Button(ribbon_frame, text=">", command=lambda: canvas.xview_scroll(1, 'units'), padx=5, pady=2)
        right_arrow.pack(side=tk.RIGHT, fill=tk.Y)

        # Add Buttons
        button_data = [
            ("Figure-of-Merit", FOM),
            ("Constraint", Constraint),
            ("Iteration", Iteration),
            ("Build", Build),
            ("Constraint Variable", Constraint_variables),
            ("Cost Variables", Cost_variables),
            ("Current Drive", Current_drive_variables),
            ("Divertor Variables", Divertor_variables),
            ("Fwbs Variables", Fwbs_variables),
            ("Heat Transport", Heat_transport_variables),
            ("Impurity Radiation", Impurity_Radiation_variables),
            ("Numerics", Numerics),
            ("CS_pfcoil", CS_pfcoil_variables),
            ("Physics Variables", Physics),
            ("Pulse Variables", Pulse),
            ("Tfcoil Variables", Tfcoil),
            ("Scan Module", None),
        ]

        # Create submenu for Scan Module
        global submenu
        submenu = tk.Menu(root, tearoff=0)
        submenu.add_command(label="1D", command=on_select_1d)
        submenu.add_command(label="2D", command=on_select_2d)

        # Add buttons to the button_container
        for text, command in button_data:
            if text == "Scan Module":
                button = tk.Button(button_container, text=text, bg="white", padx=10, pady=5)
                button.bind("<Button-1>", Scan_Module)  # Bind left click to show submenu
            else:
                button = tk.Button(button_container, text=text, command=command, bg="white", padx=10, pady=5)
            button.pack(side=tk.LEFT, padx=5, pady=5)

        # Update Scroll Region
        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        button_container.bind("<Configure>", on_configure)

        # Store reference to ribbon_frame
        root.ribbon_frame = ribbon_frame


# Initialize main application window
root = tk.Tk()
root.title("Fusion Reactor System Code ")

root.attributes('-zoomed', True)  # Works for Linux in most cases
root.geometry("800x600")

def update_checkbox_states(root):
    """Update checkbox states based on textbox content."""
    for state_key in checkbox_states:
        state_dict = checkbox_states[state_key]
        for key, value in state_dict.items():
            if value:
                if key not in text_box.get("1.0", tk.END).strip():
                    state_dict[key] = False
                    for widget in root.winfo_children():
                        if isinstance(widget, tk.Toplevel):
                            for child in widget.winfo_children():
                                if isinstance(child, tk.Canvas):
                                    for item in child.winfo_children():
                                        if isinstance(item, tk.Frame):
                                            for checkbox in item.winfo_children():
                                                if isinstance(checkbox, tk.Checkbutton):
                                                    if checkbox.cget("text") == key:
                                                        checkbox.deselect()
    root.after(100, lambda: update_checkbox_states(root))  # Call this function again after 100ms


# Call the update_checkbox_states function initially
update_checkbox_states(root)

# Global variables
current_file_path = None
night_mode = False

# Create menu bar
menu_bar = tk.Menu(root)

# 'File' menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open File", command=open_file)
file_menu.add_command(label="Save", command=save)
file_menu.add_command(label="Save As", command=save_as)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu, underline=0)

# 'Edit' menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Undo", command=undo_action)
edit_menu.add_command(label="Redo", command=redo_action)
edit_menu.add_command(label="Find", command=find_text)
edit_menu.add_command(label="Find & Replace", command=find_and_replace)
edit_menu.add_command(label="Zoom In", command=zoom_in)
edit_menu.add_command(label="Zoom Out", command=zoom_out)
menu_bar.add_cascade(label="Edit", menu=edit_menu, underline=0)

# 'View' menu
view_menu = tk.Menu(menu_bar, tearoff=0)
view_menu.add_checkbutton(label="Night Mode", command=toggle_night_mode)
menu_bar.add_cascade(label="View", menu=view_menu, underline=0)

# 'Variables' menu
menu_bar.add_command(label="Variables", command=new2_simple_ribbon)

# Configure the menu bar
root.config(menu=menu_bar)

# Create a scrollable text box
text_box = ScrolledText(root, wrap=tk.WORD, font=("Arial", 12), undo=True, fg="black", insertbackground="black")
text_box.pack(expand=True, fill=tk.BOTH)

# Ensure proper undo/redo checkpoints
def track_text_changes(event=None):
    text_box.edit_separator()
    
text_box.bind("<KeyRelease>", track_text_changes)
text_box.bind("<Delete>", track_text_changes)

# Create a footer frame and add the Execute button
footer = tk.Frame(root)
footer.pack(side="bottom", fill="x")

summery_button = tk.Button(footer, text="Summary", command=summary_command)
summery_button.pack(side="right", padx=10, pady=10)

execute_button = tk.Button(footer, text="Execute", command=execute_command)
execute_button.pack(side="right", padx=10, pady=10)


# Bind shortcuts
root.bind("<Control-o>", lambda event: open_file())
root.bind("<Control-s>", lambda event: save())
root.bind("<Control-Shift-S>", lambda event: save_as())
root.bind("<Control-q>", lambda event: root.quit())
root.bind("<Control-z>", lambda event: undo_action())
root.bind("<Control-y>", lambda event: redo_action())
root.bind("<Control-f>", lambda event: find_text())
root.bind("<Control-h>", lambda event: find_and_replace())
root.bind("<Control-plus>", lambda event: zoom_in())
root.bind("<Control-minus>", lambda event: zoom_out())



# Run the application
root.mainloop()

