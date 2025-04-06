# All the functions related to running scans
import os
from pathlib import Path
from datetime import datetime
import shelve
import dbm.dumb

# Force shelve to use dbm.dumb backend
shelve.DbfilenameShelf = shelve.Shelf
shelve.open = lambda *args, **kwargs: shelve.Shelf(dbm.dumb.open(*args, **kwargs))


# Initializes the scan process and returns the final filesystem dictionary
def runScan():
    print("Running Scan")
    home_dir = Path.home()     
    files_tree = {}
    
    with shelve.open(str(Path(Path.home(), '.dust_fox', 'df_user.shelve'))) as settings_dict:
        files_tree = expand_dir(str(home_dir.resolve()), settings_dict)
    
    print("scan done")
    return files_tree


# Checks whitelist/blacklist and hidden directory settings against a file
def is_scanned(root, settings):
    normalized_root = os.path.normpath(root) 
    root_separated = normalized_root.split(os.sep)
    
    if root == str(Path.home()):
        return True

    if not settings["scan_hidden_dirs"] and any(part.startswith('.') for part in root_separated):
        return False
            
    in_whitelist = any(root.startswith(path) for path in settings["whitelist"])
    in_blacklist = any(root.startswith(path) for path in settings["blacklist"])
    if in_whitelist and not in_blacklist:
        return True
    


def get_time(timestamp):
    date = datetime.fromtimestamp(timestamp)
    return date.strftime("%Y-%m-%d %H:%M:%S")


def get_filestats(file_object, settings):
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
    
    # Check whether to include the file
    is_old = all((datetime.now() - datetime.fromtimestamp(time)).total_seconds()  > settings["days_since_touch"] * 86400 for time in [stats.st_atime, stats.st_mtime])
    
    
    if is_old and is_scanned(file_dict["path"], settings):
        return file_dict
    else:
        return False


def expand_dir(pathname, settings):
    
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
                    
                    if is_scanned(item.path, settings):
                        item_dict = expand_dir(item.path, settings)
                        
                        # As long as there is at least one file or subdirectory
                        if item_dict["dirs"] or item_dict["files"]:
                            dir_dict['dirs'][item.path] = item_dict
                    
                # If the item is a file
                elif item.is_file():
                    filestats = get_filestats(item, settings)
                    if filestats:
                        dir_dict['files'][item.path] = filestats
            
            # Skip directories we don't have permission to touch anyways
            except PermissionError as e:
                print(f"Insufficient permissions on path object: {e}")
    
      
              
    return dir_dict
    
    
    