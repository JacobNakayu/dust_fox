# Functions to manipulate and interact with the scan results
import os, platform, subprocess
from send2trash import send2trash
from settings_functions import edit_settings

def deleteFiles(treeview):
    print("deleting file")
    for filepath in treeview.selection():
        treeview.delete(filepath)
        send2trash(filepath)

    return

def openFiles(treeview):
    print("opening file")
    
    for filepath in treeview.selection():
        # Check what operating system it is
        if platform.system() == 'Darwin': # MacOS
            subprocess.call((open, filepath))
        if platform.system() == 'Windows':
            os.startfile(filepath)
        else: # Linux
            subprocess.call(('xdg-open', filepath))
    return

def excludeFiles(treeview):
    print("excluding file")
    for filepath in treeview.selection():
        print(filepath)
        edit_settings({"blacklist": filepath}, "append")
        treeview.delete(filepath)
    
    return