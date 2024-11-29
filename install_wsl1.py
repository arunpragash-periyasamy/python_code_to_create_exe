import sys
import os
import shutil
import subprocess
import logging

import winshell  # Install with `pip install winshell`
from win32com.client import Dispatch

from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from datetime import datetime

def log_function_entry_exit(func):
    """Decorator to log entry and exit of functions."""
    def wrapper(*args, **kwargs):
        logging.info(f"Entering function: {func.__name__}")
        result = func(*args, **kwargs)
        logging.info(f"Exiting function: {func.__name__}")
        return result
    return wrapper



def update_logs(message):
    # Get the current time and format it
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format the datetime as a string
    
    # Write the formatted datetime and message to the file
    with open("logging.txt", 'a') as file:
        file.write(current_time + " " + message + "\n")  # Add newline at the end for each log entry




def configure_logging():
    """Set up logging for the application."""
    log_file = "application.log"
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    logging.info("Logging configured. Outputting to %s", log_file)


# def configure_logging():
#     """Set up logging for the application."""
#     log_file = "application.log"
#     log_dir = os.path.dirname(log_file)
#     if not os.path.exists(log_dir):
#         os.makedirs(log_dir)

#     logging.basicConfig(
#         level=logging.DEBUG,
#         format='%(asctime)s - %(levelname)s - %(message)s',
#         handlers=[
#             logging.FileHandler(log_file),
#             logging.StreamHandler(sys.stdout)
#         ]
#     )

#     # Ensure log entries are flushed immediately
#     logging.info("Logging configured. Outputting to %s", log_file)




@log_function_entry_exit
def start_gui():
    """Start the GUI application."""
    logging.info("Starting GUI application...")
    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("Embedded Web App")

    browser = QWebEngineView()
    browser.setUrl(QUrl("http://localhost:9000"))

    layout = QVBoxLayout()
    layout.addWidget(browser)

    container = QWidget()
    container.setLayout(layout)
    window.setCentralWidget(container)

    window.resize(1024, 768)
    window.show()
    app.exec()


@log_function_entry_exit
def create_shortcut():
    """Create a desktop shortcut for the application."""
    logging.info("Creating desktop shortcut...")
    desktop = winshell.desktop()
    shortcut_path = os.path.join(desktop, "MyApp.lnk")
    target = sys.executable
    icon = os.path.join(os.path.dirname(target), "app.ico")

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = target
    shortcut.WorkingDirectory = os.path.dirname(target)
    shortcut.IconLocation = icon
    shortcut.save()
    logging.info("Shortcut created at %s", shortcut_path)


@log_function_entry_exit
def get_tar_file_path():
    """Get the path to the embedded tar file."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, "infogreen-cloudbook.tar")
    else:
        return "infogreen-cloudbook.tar"


@log_function_entry_exit
def extract_tar_file():
    """Extract the embedded tar file to a temporary location."""
    tar_path = get_tar_file_path()
    logging.info(f"Extracting tar file from {tar_path}...")
    if not os.path.exists(tar_path):
        logging.error(f"Tar file {tar_path} does not exist.")
        sys.exit(1)

    extracted_file = "infogreen-cloudbook.tar"
    shutil.copyfile(tar_path, extracted_file)
    logging.info(f"Extracted tar file to {extracted_file}")
    return extracted_file


@log_function_entry_exit
def is_wsl_installed():
    """Check if WSL is installed."""
    try:
        # Check if WSL is present and supports --version (available in WSL 2 and later)
        result = subprocess.run(["wsl", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        logging.info("WSL is installed.")
        logging.debug(f"WSL version output: {result.stdout.decode().strip()}")
        return True
    except subprocess.CalledProcessError as e:
        logging.warning(f"WSL version check failed: {e}. Output: {e.stdout.decode()} {e.stderr.decode()}")
    except FileNotFoundError:
        logging.warning("WSL is not installed or not available.")

    # Fallback check: Test if the `wsl` command exists (for older systems)
    try:
        result = subprocess.run(["wsl", "--help"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        logging.info("WSL is installed but might not support `--version`.")
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        logging.error("WSL is not installed or not functional.")
        return False


@log_function_entry_exit
def install_wsl():
    """Install WSL if not already installed."""
    logging.info("Attempting to install WSL...")
    try:
        subprocess.run(["wsl", "--install"], check=True)
        logging.info("WSL installation completed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during WSL installation: {e}")
        logging.error(f"Command output: {e.stdout.decode()} {e.stderr.decode()}")
        sys.exit(1)
    except FileNotFoundError:
        logging.critical("WSL installation command not found. Ensure you are running on a supported Windows version.")
        sys.exit(1)



@log_function_entry_exit
def import_wsl_instance(tar_file, instance_name):
    """Import the provided tar file into a new WSL instance."""
    if not os.path.exists(tar_file):
        logging.error(f"Error: The file '{tar_file}' does not exist.")
        sys.exit(1)

    logging.info(f"Importing '{tar_file}' as WSL instance '{instance_name}'...")
    target_dir = f"C:\\WSL\\{instance_name}"
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    os.makedirs(target_dir, exist_ok=True)

    try:
        subprocess.run(["wsl", "--import", instance_name, target_dir, tar_file], check=True)
        logging.info(f"WSL instance '{instance_name}' imported successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error importing WSL instance: {e}")
        sys.exit(1)


@log_function_entry_exit

def execute_commands_in_instance(instance_name):
    """Log in to the WSL instance and execute specified commands."""
    commands = [
        "cd /usr/backend",
        "docker pull arunpragash/angular_todo:1.1",
        "docker run -d -p 9000:80 arunpragash/angular_todo:1.1",
        "docker compose up --build -t"
    ]
    update_logs("Before for loops for the commands")
    for command in commands:
        try:
            update_logs(instance_name + " " + command + " inside the for loop")
            logging.info(f"Executing command in WSL instance '{instance_name}': {command}")
            result = subprocess.run(
                ["wsl", "-d", instance_name, "bash", "-c", command],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            logging.info(f"Command output:\n{result.stdout.decode() if result.stdout else 'No output'}")
            if result.stderr:
                logging.warning(f"Command error:\n{result.stderr.decode()}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error executing command '{command}': {e}")
        except Exception as e:
            logging.error(f"Unexpected error during command '{command}': {e}")
    update_logs("After for loops for the commands")
# def execute_commands_in_instance(instance_name):
#     """Log in to the WSL instance and execute specified commands."""
#     commands = [
#         "cd /usr/backend",
#         "docker pull arunpragash/angular_todo:1.1",
#         "docker run -d -p 9000:80 arunpragash/angular_todo:1.1",
#         "docker compose up --build -t"
#     ]
#     update_logs("Before for loops for the commands")
#     for command in commands:
#         try:
#             update_logs(instance_name +" " +command + " inside the for loop")
#             logging.info(f"Executing command in WSL instance '{instance_name}': {command}")
#             result = subprocess.run(
#                 ["wsl", "-d", instance_name, "bash", "-c", command],
#                 check=True,
#                 stdout=subprocess.PIPE,
#                 stderr=subprocess.PIPE
#             )
#             update_logs(instance_name +" " +command + " inside the for loop")
#             logging.info(f"Command output:\n{result.stdout.decode()}")
#             if result.stderr:
#                 logging.warning(f"Command error:\n{result.stderr.decode()}")
#         except subprocess.CalledProcessError as e:
#             logging.error(f"Error executing command '{command}': {e}")
#             sys.exit(1)

#     update_logs("After for loops for the commands")


@log_function_entry_exit
# def main():
#     try:
#         logging.info("Program started")
#         configure_logging()
#         instance_name = "cloudbook"
        
#         if not is_wsl_installed():
#             logging.info("WSL is not installed. Attempting installation...")
#             install_wsl()

#         tar_file = extract_tar_file()
#         import_wsl_instance(tar_file, instance_name)
#         execute_commands_in_instance(instance_name)
#         create_shortcut()
#         start_gui()
#     except Exception as e:
#         logging.error(f"An unexpected error occurred: {e}", exc_info=True)
#         sys.exit(1)

def main():
    update_logs("Starting the configuration logging")
    configure_logging()
    update_logs("Ended the configuration logging")
    instance_name = "cloudbook"

    if not is_wsl_installed():
        logging.info("WSL is not installed. Attempting installation...")
        update_logs("Before installing WSL")
        install_wsl()
        update_logs("After installing WSL")

    tar_file = extract_tar_file()
    update_logs("Before importing WSL instance")
    import_wsl_instance(tar_file, instance_name)
    update_logs("After importing WSL instance")
    update_logs("Before commands in WSL instance")
    execute_commands_in_instance(instance_name)
    update_logs("After commands in WSL instance")
    update_logs("Before creating shortcuts")
    create_shortcut()
    update_logs("After creating shortcuts")
    update_logs("Before GUI")
    start_gui()
    update_logs("After GUI")





if __name__ == "__main__":
    main()
