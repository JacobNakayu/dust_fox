# UI Packages
import tkinter as tk
from tkinter import ttk
# Other Packages
from pathlib import Path
# Fonts
from styles import MAIN_TITLE, BODY_TEXT
# Custom Widgets
from widgets import ScrollableFrame, FileTree
# Global variables
from settings import MIN_WIDTH, MIN_HEIGHT
# Functions
from scan_functions import runScan
from results_functions import deleteFiles, openFiles, excludeFiles
from settings_functions import load_defaults

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
        delete_button = ttk.Button(self, text="Delete File", command=lambda: deleteFiles())
        delete_button.grid(row=3, column=0, padx=10, pady=10)
        open_file_button = ttk.Button(self, text="Open File", command=lambda: openFiles())
        open_file_button.grid(row=3, column=1, padx=10, pady=10)
        exclude_file_button = ttk.Button(self, text="Exclude File", command=lambda: excludeFiles())
        exclude_file_button.grid(row=3, column=2, padx=10, pady=10)
    
    def scan_from_click(self):
        self.scan_results = runScan()
        # with open('./dataview.json', 'w') as file:
        #     import json
        #     from pathlib import Path
        #     print(Path.cwd())
        #     file.write(json.dumps(self.scan_results))
        
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
        
        # Configure the grid
        for i in range(0,3):
            self.grid_columnconfigure(i, weight=1)
            
        # Configure rows to allow vertical centering 
        # Makes the space above and below the content expand when the window enlarges
        self.grid_rowconfigure(0, weight=1)  # Space above title
        self.grid_rowconfigure(4, weight=1)  # Space below buttons
        
        # Title of the page (text, font, and placement)
        label = ttk.Label(self, text="Settings Page", font = MAIN_TITLE)
        label.grid(row=0, column=1, padx=10, pady=10)


if load_defaults():        
    app = DustFoxApp()
    app.mainloop()
else:
    print("Could not load save file. Aborting...")