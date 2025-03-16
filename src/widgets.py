import  tkinter as tk
from tkinter import ttk
from uuid import uuid4

# A frame with X and Y scroll bars
class ScrollableFrame(tk.Frame):
    def __init__(self, parent, min_width, min_height, *args, **kwargs):
        # Initialize the Frame class
        super().__init__(parent, *args, **kwargs)
        
        # Minimum size variables
        self.min_width = min_width
        self.min_height = min_height
        
        # Create a canvas to allow scrolling and an inner frame to hold the content
        self.canvas = tk.Canvas(self)
        self.scrollable_frame = tk.Frame(self.canvas)
                
        # Attach the inner frame to the canvas using a Window
        self.canvas_frame = self.canvas.create_window((0,0), window=self.scrollable_frame, anchor="nw")
        
        # Vertical scrollbar
        self.v_scroll = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.v_scroll.set)
        
        # Horizontal scrollbar
        self.h_scroll = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.canvas.config(xscrollcommand=self.h_scroll.set)
        
        # Layout
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.v_scroll.grid(row=0, column=1, sticky="ns")
        self.h_scroll.grid(row=1, column=0, sticky="we")
        
        # Allow the outer frame to expand as needed
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Update the scrollregion when the outer frame changes size
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        
        # Expand the inner frame to fit the whole canvas
        self.canvas.bind("<Configure>", self.setFrameWidth)
        
        # Bind the mouse wheel for scrolling
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)
        
    # Updates the scrollable region to cover the inner frame   
    def on_frame_configure(self, event):
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
    
    # Scrolls a certain amount based on the mouse wheel direction
    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    # Allow the inner frame to resize and fill the Canvas down to a set of minimum dimensions
    def setFrameWidth(self, event):
        # Check if the window is smaller than the minimum dimensions
        new_width = event.width if event.width > self.min_width else self.min_width
        new_height = event.height if event.height > self.min_height else self.min_height
        
        if new_width != self.scrollable_frame.winfo_width():
            self.canvas.itemconfig(self.canvas_frame, width=new_width - 4)
        if new_height != self.scrollable_frame.winfo_height():
            self.canvas.itemconfig(self.canvas_frame, height=new_height - 4) 
            

# Creates an expandible tree structure from a filesystem dictionary
class FileTree(ttk.Treeview):
    def __init__(self, parent, file_tree, *args, **kwargs):
        # Initialize the Frame class
        super().__init__(parent, *args, **kwargs)
        
        # Specify how many columns there are, what size they are, and what they are called
        columnnames = ["Size", "Created", "Accessed", "Modified"]
        self.config(columns=columnnames)
        for col in columnnames:
            self.heading(col, text=col)
        
        self.column("Size", width=100, anchor="center")
        self.column("Created", width=150, anchor="center")
        self.column("Accessed", width=150, anchor="center")
        self.column("Modified", width=150, anchor="center")
        
        # Load the filesystem starting at the home directory
        self.load_file_tree('', file_tree)
        
    # Takes the filesystem dictionary and loads it into the ttk Treeview structure
    def load_file_tree(self, parent, file_tree):
        # If the current object is a directory
        if "dirs" in file_tree.keys():
            # For every subdirectory
            for dir_path in file_tree["dirs"].keys():
                # Create a unique id so we can identify it later
                uid = uuid4()
                # Add a line showing the name of the directory
                self.insert(parent, 'end', uid, text=file_tree["dirs"][dir_path]["name"])
                # Recursively call this function on the subdirectory
                self.load_file_tree(uid, file_tree["dirs"][dir_path])
            
            # For every file
            for file_path in file_tree["files"].keys():
                file_object = file_tree["files"][file_path]
                # Create a unique id
                uid = uuid4()
                # Add a line showing all the relevant info for the file
                self.insert(parent, 'end', uid,\
                    text=file_object["name"],\
                        values=[file_object["size"],\
                                file_object["created"],\
                                file_object["accessed"],\
                                file_object["modified"]])
        