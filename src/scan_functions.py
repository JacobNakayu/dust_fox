# All the functions related to running scans
import os
from pathlib import Path
from datetime import datetime
import shelve

def runScan():
    print("Running Scan")
    home_dir = Path.home()     
    files_tree = {}
    
    # for root, dirs, files in os.walk(home_dir):
    #     if is_scanned(root):
    #         files_tree[root] = {
    #             "path": root,
    #             "name": root.split('\\')[-1],
    #             "dirs": [directory for directory in dirs if is_scanned(os.path.join(root, directory))],
    #             # "files": [file for file in files if is_scanned(os.path.join(root, file))]
    #             "files": [get_filestats(os.path.join(root, file)) for file in files if is_scanned(os.path.join(root, file))]
    #         }
     
    files_tree = expand_dir(str(home_dir.resolve()))
    print("scan done")
    return files_tree


def is_scanned(root):
    settings = shelve.open(str(Path(Path.home(), '.dust_fox', 'df_user.shelve')))
    
    root_separated = root.split('\\')
    
    if root == str(Path.home()):
        return True

    if not settings["scan_hidden_dirs"] and any(part.startswith('.') for part in root_separated):
        return False
            
    is_allowed = any(root.startswith(path) for path in settings["directory_list"])
    if (settings["use_whitelist"] and is_allowed) or (not settings["use_whitelist"] and not is_allowed):
        return True
    


def get_time(timestamp):
    date = datetime.fromtimestamp(timestamp)
    return date.strftime("%Y-%m-%d %H:%M:%S")

def get_filestats(file_object):
    # stats = file_object.stat()
    stats = os.stat(file_object)
    file_dict = {
        "path": file_object.path,
        "name": file_object.path.split('\\')[-1],
        "size": f"{stats.st_size} B" if stats.st_size < 1000 
                else f"{round(stats.st_size / 1000, 2)} kB" if stats.st_size < 1000000 \
                else f"{round(stats.st_size / 1000000, 2)} MB" if stats.st_size < 1000000000 \
                else f"{round(stats.st_size / 1000000000, 2)} GB",
        "created": get_time(stats.st_birthtime),
        "accessed": get_time(stats.st_atime),
        "modified": get_time(stats.st_mtime)
    }

    return file_dict


def expand_dir(pathname):
    # Get the settings shelf
    settings = shelve.open(str(Path(Path.home(), '.dust_fox', 'df_user.shelve')))
    
    # Establish the base structure for the directory dictionary
    dir_dict = {
        "path": pathname,
        "name": pathname.split('\\')[-1],
        "dirs": {},
        "files": {}  
    }
    
    # Enumerate the directory
    with os.scandir(pathname) as dir:
        for item in dir:
            try:
                # If the item is a directory
                if item.is_dir():
                    # Skip hidden directories if scanning them is disabled
                    if not settings["scan_hidden_dirs"] and item.name.startswith("."):
                        continue
                    
                    # Check if the file matches the whitelist or blacklist condition
                    is_allowed = any(item.path.startswith(path) for path in settings["directory_list"])
                    if (settings["use_whitelist"] and is_allowed) or (not settings["use_whitelist"] and not is_allowed):
                        dir_dict['dirs'][item.path] = expand_dir(item.path)
                    
                # If the item is a file
                elif item.is_file():
                    dir_dict['files'][item.path] = get_filestats(item)
            
            # Skip directories we don't have permission to touch anyways
            except PermissionError as e:
                print(f"Insufficient permissions on path object: {e}")
                
    return dir_dict
    
    
    