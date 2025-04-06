# UI Packages
import tkinter as tk
from tkinter import ttk
# Other Packages
from pathlib import Path
import shelve
import dbm.dumb
import sys
# Fonts
from styles import MAIN_TITLE
# Custom Widgets
from widgets import ScrollableFrame, FileTree, FilterListTree
# Global variables
from settings import MIN_WIDTH, MIN_HEIGHT
# Functions
from scan_functions import runScan
from results_functions import deleteFiles, openFiles, excludeFiles
from settings_functions import load_defaults, edit_settings, revert_settings

# Force shelve to use dbm.dumb backend
shelve.DbfilenameShelf = shelve.Shelf
shelve.open = lambda *args, **kwargs: shelve.Shelf(dbm.dumb.open(*args, **kwargs))

# Main App Window
class DustFoxApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        # Initialize a basic application window
        super().__init__(*args, **kwargs)
        
        # Set the initial load size and name the window
        self.geometry(f"{MIN_WIDTH + 20}x{MIN_HEIGHT + 20}")
        self.title("Dust Fox")
        
        # Navigational Menu
        menu_bar = tk.Menu(self)
        menu_bar.add_command(label="Scan", command=lambda: self.show_frame(ScanPage))
        menu_bar.add_command(label="Settings", command=lambda: self.show_frame(SettingsPage))
        self.config(menu=menu_bar)
        
        # Create a Scrollable Frame to hold the content
        main_frame = ScrollableFrame(self, MIN_WIDTH, MIN_HEIGHT)
        # Place it at the top, stretch it to fill all available space, allow it to expand
        main_frame.pack(side='top', fill='both', expand=True)
        
        # Use the inner frame of the Scrollable Frame as the container for the pages
        content_frame = main_frame.scrollable_frame
        
        # Configure the content frame grid
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)        
        
        # Initialize a dictionary of different views within the app
        self.frames = {}
        
        # Initialize each page into the frames dictionary
        for F in (ScanPage, SettingsPage):
            # Set the parent of the page to be the main container and the controller to be the app
            frame = F(content_frame, self)
            # Puts the view in the dictionary using the class as the key
            self.frames[F] = frame
            # Stacks all the views on top of each other
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Specify which frame to start with
        self.show_frame(ScanPage)
        
    # Method to display a frame,  where Content is the class name of the page
    def show_frame(self, content):
        # Retrieve the specified frame from the dictionary
        frame = self.frames[content]
        
        # Update the cached settings
        try:
            frame.get_settings()
        except:
           pass 
        
        # Bring that page to the top of the stack
        frame.tkraise()
        


# Main page for the application
class ScanPage(tk.Frame):
    # Pass in the parent container and the controlling application
    def __init__(self, parent, controller):
        # Initialize the Frame class
        super().__init__(parent)
        
        # Initialize the results array
        self.scan_results = []
        
        # Configure the grid
        for i in range(0,3):
            self.grid_columnconfigure(i, weight=1)
        
        for i in range(0,4):
            self.grid_rowconfigure(i, weight=1)
        
        # Button to run scan
        scan_button = ttk.Button(self, text="Scan for Old Files", command=lambda: self.scan_from_click())
        scan_button.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Current directory label
        self.cwd_label = ttk.Label(self, text=("No Scan Results"), background="white", anchor="center")
        self.cwd_label.grid(row=1, column=0, columnspan=3, pady=10, sticky="we")
        
        # Results widget
        results_panel = ScrollableFrame(self, 500, 0)
        results_panel.grid(row=2, column=0, columnspan=3, padx=10, sticky="we")
        self.results_frame = results_panel.scrollable_frame
        self.results_frame.config(bg="white")
    
        self.results_frame.grid_columnconfigure(0, weight=1)
        
        # Action Buttons
        delete_button = ttk.Button(self, text="Delete Files", command=lambda: deleteFiles(self.results_tree))
        delete_button.grid(row=3, column=0, padx=10, pady=10)
        open_file_button = ttk.Button(self, text="Open Files", command=lambda: openFiles(self.results_tree))
        open_file_button.grid(row=3, column=1, padx=10, pady=10)
        exclude_file_button = ttk.Button(self, text="Exclude Files", command=lambda: excludeFiles(self.results_tree))
        exclude_file_button.grid(row=3, column=2, padx=10, pady=10)
    
    def scan_from_click(self):
        self.scan_results = runScan()
        
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        self.results_tree = FileTree(self.results_frame, self.scan_results)
        self.results_tree.grid(row=0, column=0, sticky="nsew")
        
        self.cwd_label.config(text=str(Path.home().resolve()))
            
        

class SettingsPage(tk.Frame):
    # Pass in the parent container and the controlling application
    def __init__(self, parent, controller):
        # Initialize the Frame class
        super().__init__(parent)
        
        self.temp_settings = {"whitelist":[], "blacklist":[]}
        
        # Configure the grid
        for i in range(0,6):
            self.grid_columnconfigure(i, weight=1)
            
        for i in range (0,7):
            self.grid_rowconfigure(i, weight=1)
            
        # Configure rows to allow vertical centering 
        # Makes the space above and below the content expand when the window enlarges
        # self.grid_rowconfigure(0, weight=1)  # Space above title
        # self.grid_rowconfigure(4, weight=1)  # Space below buttons
        
        # Title of the page (text, font, and placement)
        page_title = ttk.Label(self, text="Settings", font = MAIN_TITLE)
        page_title.grid(row=0, column=0, columnspan=6, padx=10, pady=10)
        
        # Settings labels and inputs
        
        # Time setting
        time_label = ttk.Label(self, text="Look for Files Not Touched In:", anchor="center")
        self.time_dropdown = ttk.Combobox(self, state="readonly", values=["7 Days", "14 Days", "30 Days", "60 Days", "90 Days", "180 Days", "365 Days"])
        
        time_label.grid(row=1, column=0, columnspan=3, sticky="we")
        self.time_dropdown.grid(row=1, column=3, columnspan=3, sticky="we")
        
        # Hidden directory toggle
        hidden_dirs_label = ttk.Label(self, text="Scan Hidden Directories and Files:", anchor="center")
        self.hidden_dirs_dropdown = ttk.Combobox(self, state="readonly", values=["True", "False"])
        
        hidden_dirs_label.grid(row=2, column=0, columnspan=3, sticky="we")
        self.hidden_dirs_dropdown.grid(row=2, column=3, columnspan=3, sticky="we")
        
        # Whitelist Editing
        whitelist_label = ttk.Label(self, text="Scan These")
        self.whitelist_box = FilterListTree(self, self.temp_settings["whitelist"])
        whitelist_new_path = ttk.Entry(self)
        whitelist_add = ttk.Button(self, text="Add Path", command=lambda: self.action_path("add", whitelist_new_path.get(), self.temp_settings["whitelist"], self.whitelist_box))
        whitelist_drop = ttk.Button(self, text="Remove Selected", command=lambda: self.action_path("drop", self.whitelist_box.selection(), self.temp_settings["whitelist"], self.whitelist_box))
                    
        whitelist_label.grid(row=3, column=0, columnspan=3)
        self.whitelist_box.grid(row=4, column=0, columnspan=3, sticky="we", padx=10)
        whitelist_drop.grid(row=5, column=0, columnspan=3, sticky="we", padx=10)
        whitelist_add.grid(row=6, column=0, sticky="we", padx=10)
        whitelist_new_path.grid(row=6, column=1, columnspan=2, sticky="we", padx=10)
        
        
        # Blacklist Editing
        blacklist_label = ttk.Label(self, text="Do Not Scan")
        self.blacklist_box = FilterListTree(self, self.temp_settings["blacklist"])
        blacklist_new_path = ttk.Entry(self)
        blacklist_add = ttk.Button(self, text="Add Path", command=lambda: self.action_path("add", blacklist_new_path.get(), self.temp_settings["blacklist"], self.blacklist_box))
        blacklist_drop = ttk.Button(self, text="Remove Selected", command=lambda: self.action_path("drop", self.blacklist_box.selection(), self.temp_settings["blacklist"], self.blacklist_box))
        
        blacklist_label.grid(row=3, column=3, columnspan=3)
        self.blacklist_box.grid(row=4, column=3, columnspan=3, sticky="we", padx=10)
        blacklist_drop.grid(row=5, column=3, columnspan=3, sticky="we", padx=10)
        blacklist_add.grid(row=6, column=3, sticky="we", padx=10)
        blacklist_new_path.grid(row=6, column=4, columnspan=2, sticky="we", padx=10)
        
        # Action Buttons
        revert_button = ttk.Button(self, text="Revert to Default Settings", command=lambda: self.revert())
        cancel_button = ttk.Button(self, text="Cancel Changes", command=lambda: self.get_settings())
        apply_button = ttk.Button(self, text="Apply Changes", command=lambda: self.change_settings())
        
        revert_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="we")
        cancel_button.grid(row=7, column=2, columnspan=2, padx=10, pady=10, sticky="we")
        apply_button.grid(row=7, column=4, columnspan=2, padx=10, pady=10, sticky="we")

        
    def get_settings(self):
        # Get the settings
        with shelve.open(str(Path(Path.home(), '.dust_fox', 'df_user.shelve'))) as settings:
            self.temp_settings = dict(settings)
        
        time_translate = {
            7: "7 Days", 
            14: "14 Days", 
            30: "30 Days", 
            60: "60 Days", 
            90: "90 Days", 
            180: "180 Days", 
            365: "365 Days"
        }
         
        self.time_dropdown.set(time_translate[self.temp_settings["days_since_touch"]])
        self.hidden_dirs_dropdown.set("True" if self.temp_settings["scan_hidden_dirs"] else "False")
        self.whitelist_box.empty_filter_list()
        self.blacklist_box.empty_filter_list()
        self.whitelist_box.load_filter_list(self.temp_settings["whitelist"])
        self.blacklist_box.load_filter_list(self.temp_settings["blacklist"])
       
        
    def action_path(self, action, pathstring, pathlist, pathtree):
        if action == "add":
            pathlist.append(pathstring)
            pathtree.insert('', 'end', pathstring, text=pathstring)
        
        elif action == "drop":
            for path in pathstring:
                pathlist.remove(path)
                pathtree.delete(path)
                
    def change_settings(self):
        time_translate = {
            "7 Days": 7, 
            "14 Days": 14, 
            "30 Days": 30, 
            "60 Days": 60, 
            "90 Days": 90, 
            "180 Days": 180, 
            "365 Days": 365
        }
        
        settings_dict = {
            "whitelist": [path for path in self.whitelist_box.get_children()],
            "blacklist": [path for path in self.blacklist_box.get_children()],
            "days_since_touch": time_translate[self.time_dropdown.get()],
            "scan_hidden_dirs": True if self.hidden_dirs_dropdown.get() == "True" else False,
        }
        
        edit_settings(settings_dict, "overwrite")
        
        self.get_settings()
        
    def revert(self):
        revert_settings()
        self.get_settings()

import sys
print("Python:", sys.version)
print("shelve module path:", shelve.__file__)

if load_defaults():        
    app = DustFoxApp()
    app.mainloop()
else:
    print("Could not load save file. Aborting...")