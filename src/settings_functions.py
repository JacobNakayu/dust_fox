# Functions for manipulating user settings
import shelve
from pathlib import Path

# Ensures that the settings file exists and that all necessary settings exist
def load_defaults():
    settings_path = Path(Path.home(), '.dust_fox', 'df_user.shelve')
    
    try:
        if not settings_path.exists():
            # If the settings path doesn't exist, create it and the parent directory
            settings_path.parent.mkdir(exist_ok=True)
            
            # Apply the default settings
            revert_settings()

            return True
        
        else:
            # Open the settings file and list saved settings
            settings_file = shelve.open(str(settings_path), writeback=True)
            set_keys = list(settings_file.keys())
            
            # Ensure all the necessary settings exist
            # List settings
            if "whitelist" not in set_keys:
                # Populate the initial whitelist
                for dirname in ["Documents", "Downloads", "Music", "Pictures", "urMom"]:
                    # Check if the directory exists
                    dirpath = Path(Path.home(), dirname)
                    if dirpath.exists():
                        # Append 
                        settings_file["whitelist"].append(str(dirpath.resolve()))
                

            
            # Boolean Settings
            if "use_whitelist" not in set_keys:
                settings_file["use_whitelist"] = True
                
            if "scan_hidden_dirs" not in set_keys:
                settings_file["scan_hidden_dirs"] = False
            
            settings_file.close()
            return True
    
    except Exception as e:
        print(e)
        return False
    
def edit_settings(settings_dict, action):
    settings_path = Path(Path.home(), '.dust_fox', 'df_user.shelve')

    # Open the settings file and initialize the default setting
    with shelve.open(str(settings_path), writeback=True) as settings_file:
        if action == "overwrite":
            for key, value in settings_dict.items():
                if key in settings_file:
                    settings_file[key] = value
        
        elif action == "append":
            for key, value in settings_dict.items():
                if key in settings_file:
                    settings_file[key].append(value)

def revert_settings():
    settings_path = Path(Path.home(), '.dust_fox', 'df_user.shelve')
    
    # Open the settings file and initialize the default setting
    with shelve.open(str(settings_path), writeback=True) as settings_file:
        settings_file.update({
            "whitelist": [],
            "blacklist": [],
            "days_since_touch": 30,
            "scan_hidden_dirs": False,
        })
        
        # Populate the initial whitelist
        for dirname in ["Desktop", "Documents", "Downloads", "Music", "Pictures", "Videos", "OneDrive"]:
            # Check if the directory exists
            dirpath = Path(Path.home(), dirname)
            if dirpath.exists():
                # Append the main file directories to the whitelist
                settings_file["whitelist"].append(str(dirpath.resolve()))
