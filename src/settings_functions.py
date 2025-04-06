# Functions for manipulating user settings
import shelve
import dbm.dumb
from pathlib import Path


# Force shelve to use dbm.dumb backend
shelve.DbfilenameShelf = shelve.Shelf
shelve.open = lambda *args, **kwargs: shelve.Shelf(dbm.dumb.open(*args, **kwargs))


# Ensures that the settings file exists and that all necessary settings exist
def load_defaults():
    settings_path = Path(Path.home(), '.dust_fox', 'df_user.shelve')
    
    try:
        try:
            # Open the settings file and list saved settings
            with shelve.open(str(settings_path)) as settings_file:
                set_keys = list(settings_file.keys())
                
                # Ensure all the necessary settings exist
                # List settings
                if "whitelist" not in set_keys:
                    # Populate the initial whitelist
                    temp_whitelist = settings_file["whitelist"]
                    for dirname in ["Documents", "Downloads", "Music", "Pictures", "urMom"]:
                        # Check if the directory exists
                        dirpath = Path(Path.home(), dirname)
                        if dirpath.exists():
                            # Append 
                            temp_whitelist.append(str(dirpath.resolve()))
                    
                    settings_file["whitelist"] = temp_whitelist
                
                # Boolean Settings
                if "use_whitelist" not in set_keys:
                    settings_file["use_whitelist"] = True
                    
                if "scan_hidden_dirs" not in set_keys:
                    settings_file["scan_hidden_dirs"] = False
                
                settings_file.sync()
            return True
        
        except:
            # If the settings path doesn't exist, create it and the parent directory
            settings_path.parent.mkdir(exist_ok=True)
            
            # Apply the default settings
            revert_settings()

            return True
    
    except Exception as e:
        print(e)
        return False
    
def edit_settings(settings_dict, action):
    settings_path = Path(Path.home(), '.dust_fox', 'df_user.shelve')

    # Open the settings file and initialize the default setting
    with shelve.open(str(settings_path)) as settings_file:
        if action == "overwrite":
            for key, value in settings_dict.items():
                if key in settings_file:
                    settings_file[key] = value
            
        
        elif action == "append":
            for key, value in settings_dict.items():
                temp_list = settings_file[key]
                if key in settings_file:
                    temp_list.append(value)
                settings_file[key] = temp_list
        
        settings_file.sync()

def revert_settings():
    settings_path = Path(Path.home(), '.dust_fox', 'df_user.shelve')
    
    # Open the settings file and initialize the default setting
    with shelve.open(str(settings_path)) as settings_file:
        settings_file.update({
            "whitelist": [],
            "blacklist": [],
            "days_since_touch": 30,
            "scan_hidden_dirs": False,
        })
        
        # Populate the initial whitelist
        temp_whitelist = settings_file["whitelist"]
        for dirname in ["Desktop", "Documents", "Downloads", "Music", "Pictures", "Videos", "OneDrive"]:
            # Check if the directory exists
            dirpath = Path(Path.home(), dirname)
            if dirpath.exists():
                # Append the main file directories to the whitelist
                temp_whitelist.append(str(dirpath.resolve()))
        
        settings_file["whitelist"] = temp_whitelist

        settings_file.sync()