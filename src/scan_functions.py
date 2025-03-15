# All the functions related to running scans
import os
from pathlib import Path
from datetime import datetime
import shelve

def runScan():
    print("Running Scan")
    home_dir = Path.home()
    files_dict = {}
    settings = shelve.open(Path(home_dir, '.dust_fox', 'df_user.shelve').name)
    
    files_tree = expand_dir(str(home_dir.resolve()))
    
    return files_tree
    # for root, dirs, files in os.walk(home_dir):
    #     file_data = {
    #         "root": root,
    #         "dirs": dirs,
    #         "files": files,
    #     }
        
    #     if not settings["scan_hidden_dirs"]:
    #         if "\\." not in file_data["root"] and "/." not in file_data["root"]:
    #             files_dict[root] = file_data
    #     else:
    #         files_dict.append(file_data)
    # return files_dict

def get_time(timestamp):
    date = datetime.fromtimestamp(timestamp)
    return date.strftime("%Y-%m-%d %H:%M:%S")

def get_filestats(file_object):
    stats = file_object.stat()
    file_dict = {
        "path": file_object.path,
        "name": file_object.path.split('\\')[-1],
        "size": stats.st_size,
        "created": get_time(stats.st_birthtime),
        "accessed": get_time(stats.st_atime),
        "modified": get_time(stats.st_mtime)
    }

    return file_dict


def expand_dir(pathname):
    dir_dict = {
        "path": pathname,
        "name": pathname.split('\\')[-1],
        "dirs": {},
        "files": {}  
    }
    with os.scandir(pathname) as dir:
        for item in dir:
            try:
                if item.is_dir():
                    dir_dict['dirs'][item.path] = expand_dir(item.path)
                
                elif item.is_file():
                    dir_dict['files'][item.path] = get_filestats(item)
            except PermissionError as e:
                print(f"Insufficient permissions on path object: {e}")
                
    return dir_dict
    
    
    