import os
import sys
import threading
import logging
from win32com.client import Dispatch
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView


def create_shortcut():
    """Create a desktop shortcut for the application."""
    desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
    shortcut_path = os.path.join(desktop, "MyBrowser.lnk")
    target = os.path.join(sys.executable)
    icon = os.path.join(os.path.dirname(target), "infogreen.ico")

    if not os.path.exists(shortcut_path):  # Avoid creating duplicate shortcuts
        try:
            shell = Dispatch("WScript.Shell")
            shortcut = shell.CreateShortcut(shortcut_path)
            shortcut.TargetPath = target
            shortcut.WorkingDirectory = os.path.dirname(target)
            shortcut.IconLocation = icon
            shortcut.Save()
            logging.info(f"Shortcut created at {shortcut_path}")
        except Exception as e:
            logging.error(f"Failed to create shortcut: {e}")


def start_gui():
    """Start the GUI application."""
    # Create shortcut in a separate thread (if not already created)
    threading.Thread(target=create_shortcut).start()

    logging.info("Starting GUI application...")
    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("Embedded Web App")

    browser = QWebEngineView()
    browser.setUrl(QUrl("https://www.google.co.in/"))

    layout = QVBoxLayout()
    layout.addWidget(browser)

    container = QWidget()
    container.setLayout(layout)
    window.setCentralWidget(container)

    window.resize(1024, 768)
    window.show()
    app.exec()


if __name__ == "__main__":
    start_gui()
