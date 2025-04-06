# Dust Fox: For Sniffing Out Digital Dust Bunnies
Dust Fox is a simple python program built to help clean out lost clutter on your computer!

It is currently built for Python 3.13 and utilizes the modules listed in [requirements.txt](./requirements.txt). If you want to clone the git repository and run the source code locally, you'll need to install everything tagged as an "External Module" before it will work.

On the other hand, you can just [download the executable for your operating system](./executables/) and it should run right out of the box!

# How Dust Fox Works
## Running Scans
Operating Dust Fox is rather straight forward. The scanning page is shown by default when you open the program, but you can also access it by clicking on the "Scan" tab in the top left corner of the window.

1. Click the "Scan for Old Files" button at the top of the main page
2. Dust Fox will scan your computer for files that have not been opened or modified for a period of time (30 days by default)
3. Dust Fox will display a collapseable file tree with all the old files
4. You can select files or folders and choose to either move them to your trash folder, open them, or exclude them from being shown in future scan results

## Customizing Scans
Dust Fox has a few ways that you can customize what shows up in the scans. These options can be found by clicking on the "Settings" tab in the top left corner of the window.

### Time Frame
You can customize the length of time a file must have been untouched (neither opened nor modified) to qualify as "old". The default is 30 days, but there is a dropdown menu that allows you to select different time periods to scan for.

### Hidden Directories
You can also toggle Dust Fox's ability to scan hidden directories or files. These directories and files usually contain configuration files and data for other software installed on your computer, so they should generally stay put. Scanning hidden directories and files is turned off by default, but you can select "True" from the dropdown menu to enable it.

> [!Note]
> You can tell if a directory or file is hidden because it's name starts with a "." (like ".docker"). 

### Whitelist and Blacklist
Dust Fox works with a whitelist and blacklist to determine what files to scan. This means that Dust Fox will scan any file or folder in the whitelist, but only as long as it is not also in the blacklist.

> [!Note]
> Dust Fox only scans files within your account's home directory for security reasons.

For example, your whitelist could include the file paths `Documents/` and `Downloads/` and your blacklist includes the paths `private_documents/` and `very_special_file.pdf`. If you ran a scan, Dust Fox would scan every file in the Documents and Downloads folders, except for anything in a folder called private_documents folder or any file named very_special_file.pdf. Dust Fox would also not scan the `Pictures/` folder because it was not included in the whitelist (unless Pictures is within Documents or Downloads).

Dust Fox starts with some default folders in the whitelist, but you can add or remove file paths from either list as you like. It doesn't make sure the file paths you put in the "Add Path" text entries actually exist, though, so be sure to spell check yourself.

> [!Note]
> You can usually get the full path of a file by opening your file browser, right clicking on the file, and selecting "Copy as Path" (or a similar option, depending on your operating system). Just remember to take off everything up to your home directory when you paste it in to the Add Path box!

### Settings Actions
There are three buttons at the bottom of the settings page:
- Revert to Default Settings
    - Returns all the settings to what they were the first time you launched the app
- Cancel Changes
    - Returns all the settings to what they were the last time they were saved 
    - Doesn't undo Reverting to Default Settings
- Apply Changes
    - Saves the current configuration

## Uninstalling Dust Fox
There are two things you have to delete:
1. The executable file
2. The hidden directory `.dust_fox` where all the settings are stored. This should be in your account's home directory, but you may have to enable some setting in your file browser to be able to see it.
    - [Windows](https://support.microsoft.com/en-us/windows/file-explorer-in-windows-ef370130-1cca-9dc5-e0df-2f7416fe1cb1)
    - [MacOS](https://discussions.apple.com/thread/7581737?sortBy=rank)
    - Linux: Use the `-a` flag with ls in your terminal
