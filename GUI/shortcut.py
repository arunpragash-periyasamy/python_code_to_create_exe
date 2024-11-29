import os
import sys
from win32com.client import Dispatch

def create_shortcut():
    desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
    shortcut_path = os.path.join(desktop, "MyBrowser.lnk")
    target = os.path.join(os.path.dirname(sys.executable), "MyBrowser.exe")
    icon = os.path.join(os.path.dirname(sys.executable), "infogreen.ico")

    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = target
    shortcut.WorkingDirectory = os.path.dirname(target)
    shortcut.IconLocation = icon
    shortcut.Save()

if __name__ == "__main__":
    create_shortcut()
