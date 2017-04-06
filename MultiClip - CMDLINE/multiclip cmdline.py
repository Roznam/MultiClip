# MultiClip tool, used for copying to contents of .txt documents to the clipboard
# Able to navigate between directories, to enable sorting of .txt files
# Creates config file on first launch or if detecting an issue with selected MultiClip directory


#imports
import os, pyperclip
from configparser import ConfigParser

# Read / create config file if none exists
config_file = "config.ini"
config_status = 0

for i in range(2):
    if config_status == 0:
        if os.path.isfile("config.ini") == True:

            try:
                config = ConfigParser()
                config.read('config.ini')
                windowsize_cols = config.get('defaults', 'WindowSize_Cols')
                windowsize_line = config.get('defaults', 'WindowSize_Line')
                home_dir = config.get('defaults', 'MultiClipFolder')
                config_status = 1
            except:
                config_status = 0

        if config_status == 0:
            print("MultiClip configuration")

            multiclipfolder = ""
            cols = ""
            line = ""

            while multiclipfolder == "":
                entry = input("\nEnter the folderpath for the multiclip directory:\n> ")
                if os.path.isdir(entry) == True:
                    multiclipfolder = entry.upper()
                    if multiclipfolder[-1] != "\\":
                        multiclipfolder += "\\"
                else:
                    print("Invalid entry. Folderpath must point to a directory that has already been created.\n"
                          "Please try again.\n")

            while cols == "":
                try:
                    cols = int(input("\nEnter the window column size (default 80):\n> "))
                except (ValueError):
                    print("\nEntry must be an integer.")

            while line == "":
                try:
                    line = int(input("\nEnter the window line size (default 50):\n> "))
                except (ValueError):
                    print("\nEntry must be an integer.")

            f = open(config_file, "w")
            f.write(f"[defaults]\n"
                    f"MultiClipFolder = {multiclipfolder}\n"
                    f"WindowSize_Cols = {cols}\n"
                    f"WindowSize_Line = {line}")
            f.close()
            input("\nConfig file has been configured. Press any key to continue launch:\n> ")

# Set window size and title
os.system(f"mode con cols={windowsize_cols} lines={windowsize_line}")
os.system("title Multi-Clip")

# Required variables
current_dir = home_dir
home_dir = current_dir

folders_in_dir = []
files_in_dir = []
items_for_menu = []

# Program header
def header():
    cols = int(windowsize_cols)
    msg_margins = ("." * int(windowsize_cols))
    if (cols - 9) % 2 == 0:
        body = "." * int((cols - 9) / 2) + "MULTICLIP" + "." * int((cols - 9) / 2)
    else:
        body = "." * int((cols - 10) / 2) + "MULTI-CLIP" + "." * int((cols - 10) / 2)
    print(msg_margins + "\n" + body + "\n" + msg_margins + "\n")

# Call to clear screen and print header
def header_clear():
    os.system("cls")
    header()

# Prompt user to return to the main menu
def menu_return():
        input("\nPress 'Enter' to return to the main menu:")
        clear_lists()
        change_current_dir(home_dir)
        menu(home_dir)

def find_parent(folder):
    global current_dir
    current_dir = (str(os.path.abspath(os.path.join(folder, os.pardir))) + "\\")

# Change current_dir variable value
def change_current_dir(new_folder):
    global current_dir
    current_dir = new_folder

# Clear lists when changing current directory
def clear_lists():
    global folders_in_dir, files_in_dir, items_for_menu
    folders_in_dir = []
    files_in_dir = []
    items_for_menu = []

# Fetches the contents of a directory, adds results to three lists
def fetch_dir_contents(directory):
    for object in os.listdir(directory):
        object_path = directory + object

        if os.path.isfile(object_path) == True:
            files_in_dir.append(object_path)
        elif os.path.isdir(object_path) == True:
            folders_in_dir.append(object_path + "\\")

    for folder in folders_in_dir:
        items_for_menu.append(folder)
    for file in files_in_dir:
        items_for_menu.append(file)

# Copies the contents of a .txt file to the clipboard
def copy_file_contents(file):
    txt_to_copy = open((file), "r").read()
    pyperclip.copy(txt_to_copy)
    print("Copied file contents to clipboard.")

# Call when closing the program
def close():
    exit()

# Uses lists to generate menu items, folders then files
def draw_menu(folder):
    print(f"Displaying items within: {folder}")
    fetch_dir_contents(folder)
    menu_num = 1

    if current_dir.upper() == home_dir.upper():
        print("\nSelect a file to copy its contents to the clipboard.\n")
    else:
        print("\nPress 'W' to return to the main menu or 'E' to return to the parent directory.\n")

    for folders in folders_in_dir:
        print(str(menu_num) + " - " + folders[len(folder):-1])
        menu_num += 1

    for files in files_in_dir:
        print(str(menu_num) + " - " + files[len(folder):])
        menu_num += 1

    if len(items_for_menu) == 0:
        print("There are no objects within this directory to view.")

    print("\nPress 'Q' to exit")

# Allows selection of an item from the menu, redraws menu as necessary
def menu_selection():
    selection = input("\n> ")
    header_clear()

    if selection.upper() == "Q":
        close()

    if current_dir != home_dir:
        if selection.upper() == "W":
            change_current_dir(home_dir)
            clear_lists()
            menu(home_dir)

        if selection.upper() == "E":
            find_parent(current_dir)
            clear_lists()
            menu(current_dir)

    try:
        selection = (int(selection) - 1)

        # if selected item is a folder reopen the menu with the the folder contents
        if items_for_menu[selection] in folders_in_dir:
            change_current_dir(items_for_menu[selection])
            clear_lists()
            draw_menu(current_dir)
            menu_selection()

        # if selected item is a file copy the file contents to clipboard
        if items_for_menu[selection] in files_in_dir:
            copy_file_contents(items_for_menu[selection])
            menu_return()

    except (ValueError, IndexError, TypeError):
            header_clear()
            print ("Invalid entry.")
            menu_return()

# Main menu for program, prints header and available options
def menu(folder):
    header_clear()
    draw_menu(folder)
    menu_selection()

menu(home_dir)
