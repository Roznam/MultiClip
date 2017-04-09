'''
Configuration file
'''

mc_dir = "D:\\Python\\MC\\"
systray_icon = "D:\\Python\\mc.ico"

def set_mc_dir():
    new_mc_dir = input("Enter new_mc_dir :\n")
    mc_dir = new_mc_dir.strip()
    if mc_dir is None:
        set_mc_dir()

def set_systray_icon():
    new_systray_icon = input("Enter new_systray_icon :\n")
    systray_icon = new_systray_icon.strip()
    if systray_icon is None:
        set_systray_icon()
