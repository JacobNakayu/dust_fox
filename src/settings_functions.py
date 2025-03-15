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
            settings_path.touch()
            
            # Open the settings file and initialize the default setting
            settings_file = shelve.open(settings_path.name)
            settings_file.update({
                "directory_list": [],
                "use_whitelist": True,
                "scan_hidden_dirs": False,
                "scan_app_data": False,
            })
            
            # Populate the initial whitelist
            for dirname in ["Documents", "Downloads", "Music", "Pictures", "urMom"]:
                # Append 
                dirpath = str(Path(Path.home(), dirname).resolve)
            
            # Save and close the settings file
            settings_file.sync()
            settings_file.close()

            return True
        
        else:
            # Open the settings file and list saved settings
            settings_file = shelve.open(settings_path.name)
            set_keys = list(settings_file.keys())
            
            # Ensure all the necessary settings exist
            # List settings
            if "directory_list" not in set_keys:
                settings_file["directory_list"] = []
            
            # Boolean Settings
            if "use_whitelist" not in set_keys:
                settings_file["use_whitelist"] = False
                
            if "scan_hidden_dirs" not in set_keys:
                settings_file["scan_hidden_dirs"] = False
                
            if "scan_app_data" not in set_keys:
                settings_file["scan_app_data"] = False
            
            return True
    
    except:
        return False

