'''
Configuration file
'''

from configparser import ConfigParser
import os

mc_dir = None
systray_icon = None
config_file = "config.ini"

def read_config():
    '''
        Reads config.ini and sets mc_dir and systray_icon variables
    '''
    config_status = None
    try:
        global mc_dir
        global systray_icon
        config = ConfigParser()
        config.read("config.ini")
        mc_dir = config.get('DEFAULTS', 'MultiClip_Directory')
        systray_icon = config.get('DEFAULTS', 'System_Tray_Icon')
        config_status = 1
    except:
        config_status = 0
    return config_status

def write_config():
    '''
        Writes config.ini after prompting user for input via command-prompt
    '''
    print("MultiClip configuration")

    mc_dir = ""
    systray_icon = ""

    while mc_dir == "":
        entry = input("\nEnter the folderpath for MultiClip directory:\n> ").upper()
        if os.path.isdir(entry) is True:
            if entry[-1] != "\\":
                mc_dir = (entry + "\\")
        else:
            print("\nNot a valid directory. Please try again or press Ctrl+C to exit.")

    if systray_icon == "":
        if os.path.isfile("mc.ico"):
            systray_icon = "mc.ico"
        else:
            while systray_icon == "":
                entry = input("\nEnter the filepath for your System Tray .ico file:\n> ").upper()
                if os.path.isfile(entry) is True:
                    if entry[-3:] == "ICO":
                        systray_icon = entry

    f = open(config_file, "w")
    f.write(f"[DEFAULTS]\n"
            f"MultiClip_Directory = {mc_dir}\n"
            f"System_Tray_Icon = {systray_icon}\n"
            )
    f.close()
    input("\nConfig file has been configured. Press any key to close the program, then relaunch:\n> ")

def config():
    '''
        Attempts to read config, if unable to do so; writes config and then reads.
    '''
    if read_config() == 1:
        read_config()
    else:
        write_config()
        read_config()

config()
