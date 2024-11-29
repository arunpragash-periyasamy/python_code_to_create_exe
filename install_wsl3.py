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

INFO = 'info'
ERROR ='error'
DEBUG = 'debug'
WARNING = 'warning'
WSL_OUTPUT = 'wsl_output'
WSL_ERROR = 'wsl_error'



def run_wsl_commands(wsl_instance, commands, log_file, sudo_password=None):
    try:
        # Prepare the log file
        with open(log_file, 'w', newline='\n') as log:
            for command in commands:
                # Check if the command contains sudo and a password is provided
                if 'sudo' in command and sudo_password:
                    # Construct the WSL command with password piped to sudo using -S
                    wsl_command = f"wsl -d {wsl_instance} bash -c \"echo {sudo_password} | sudo -S {command}\""
                else:
                    # Construct the WSL command
                    wsl_command = f"wsl -d {wsl_instance} bash -c \"{command}\""
                
                # Run the WSL command
                result = subprocess.run(wsl_command, shell=True, text=True, capture_output=True)
                output = f"{command} {result.stdout}"
                error = f"{command} {result.stderr}"
                update_logs(output, WSL_OUTPUT)
                update_logs(error, WSL_ERROR)
                # Log the results
                log.write(f"Command: {command}\n")
                log.write(f"Output:\n{result.stdout}\n")
                log.write(f"Error (if any):\n{result.stderr}\n")
                log.write("\n" + "-" * 80 + "\n")
    except Exception as e:
        # Catch and log any exceptions
        with open(log_file, 'a', newline='\n') as log:
            log.write(f"An error occurred: {str(e)}\n")
            update_logs(f"An error occurred: {str(e)}\n", WSL_ERROR)

def log_function_entry_exit(func):
    """Decorator to log entry and exit of functions."""
    def wrapper(*args, **kwargs):
        logging.info(f"Entering function: {func.__name__}")
        update_logs(f"Entering function: {func.__name__}", INFO)
        result = func(*args, **kwargs)
        logging.info(f"Exiting function: {func.__name__}")
        update_logs(f"Exiting function: {func.__name__}", INFO)
        return result
    return wrapper



def update_logs(message, type=INFO):
    # Get the current time and format it
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format the datetime as a string
    
    if(type == INFO):
        with open("info.log", 'a') as file:
            file.write(current_time + " " + message + "\n")  # Add newline at the end for each log entry
    elif(type == DEBUG):
        with open("debug.log", 'a') as file:
            file.write(current_time + " " + message + "\n")  # Add newline at the end for each log entry
    elif(type == ERROR):
        with open("error.log", 'a') as file:
            file.write(current_time + " " + message + "\n")  # Add newline at the end for each log entry
    elif(type == WARNING):
        with open("warning.log", 'a') as file:
            file.write(current_time + " " + message + "\n")  # Add newline at the end for each log entry
    elif(type == WSL_ERROR):
        with open("wsl_error.log", 'a') as file:
            file.write(current_time + " " + message + "\n")  # Add newline at the end for each log entry
    elif(type == WSL_OUTPUT):
        with open("wsl_output.log", 'a') as file:
            file.write(current_time + " " + message + "\n")  # Add newline at the end for each log entry
    else:
        with open("others.log", 'a') as file:
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


@log_function_entry_exit
def start_gui():
    """Start the GUI application."""
    logging.info("Starting GUI application...")
    update_logs("Starting GUI application...", INFO)
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
    update_logs(f"Extracting tar file from {tar_path}...", INFO)
    if not os.path.exists(tar_path):
        logging.error(f"Tar file {tar_path} does not exist.")
        update_logs(f"Tar file {tar_path} does not exist.", ERROR)
        sys.exit(1)

    extracted_file = "infogreen-cloudbook.tar"
    shutil.copyfile(tar_path, extracted_file)
    logging.info(f"Extracted tar file to {extracted_file}")
    update_logs(f"Extracted tar file to {extracted_file}", INFO)
    return extracted_file


@log_function_entry_exit
def is_wsl_installed():
    """Check if WSL is installed."""
    try:
        # Check if WSL is present and supports --version (available in WSL 2 and later)
        result = subprocess.run(["wsl", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        logging.info("WSL is installed.")
        update_logs("WSL is installed.", INFO)
        logging.debug(f"WSL version output: {result.stdout.decode().strip()}")
        update_logs(f"WSL version output: {result.stdout.decode().strip()}", INFO)
        return True
    except subprocess.CalledProcessError as e:
        update_logs(f"WSL version check failed: {e}. Output: {e.stdout.decode()} {e.stderr.decode()}", WARNING)
        logging.warning(f"WSL version check failed: {e}. Output: {e.stdout.decode()} {e.stderr.decode()}")
    except FileNotFoundError:
        logging.warning("WSL is not installed or not available.")
        update_logs("WSL is not installed or not available.", WARNING)

    # Fallback check: Test if the `wsl` command exists (for older systems)
    try:
        result = subprocess.run(["wsl", "--help"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        logging.info("WSL is installed but might not support `--version`.")
        update_logs("WSL is installed but might not support `--version`.", INFO)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        logging.error("WSL is not installed or not functional.")
        update_logs("WSL is not installed or not functional.", ERROR)
        return False


@log_function_entry_exit
def install_wsl():
    """Install WSL if not already installed."""
    logging.info("Attempting to install WSL...")
    update_logs("Attempting to install WSL...", INFO)
    try:
        subprocess.run(["wsl", "--install", "--no-distribution"], check=True)
        logging.info("WSL installation completed successfully.")
        update_logs("WSL installation completed successfully.", INFO)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during WSL installation: {e}")
        logging.error(f"Command output: {e.stdout.decode()} {e.stderr.decode()}")
        update_logs(f"Error during WSL installation: {e}", ERROR)
        update_logs(f"Command output: {e.stdout.decode()} {e.stderr.decode()}", ERROR)
        sys.exit(1)
    except FileNotFoundError:
        logging.critical("WSL installation command not found. Ensure you are running on a supported Windows version.")
        update_logs("WSL installation command not found. Ensure you are running on a supported Windows version.", ERROR)
        sys.exit(1)



@log_function_entry_exit
def import_wsl_instance(tar_file, instance_name):
    """Import the provided tar file into a new WSL instance."""
    if not os.path.exists(tar_file):
        logging.error(f"Error: The file '{tar_file}' does not exist.")
        update_logs(f"Error: The file '{tar_file}' does not exist.", ERROR)
        sys.exit(1)

    logging.info(f"Importing '{tar_file}' as WSL instance '{instance_name}'...")
    update_logs(f"Importing '{tar_file}' as WSL instance '{instance_name}'...", INFO)
    target_dir = f"C:\\WSL\\{instance_name}"
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    os.makedirs(target_dir, exist_ok=True)

    try:
        subprocess.run(["wsl", "--import", instance_name, target_dir, tar_file], check=True)
        logging.info(f"WSL instance '{instance_name}' imported successfully.")
        update_logs(f"WSL instance '{instance_name}' imported successfully.", INFO)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error importing WSL instance: {e}")
        update_logs(f"Error importing WSL instance: {e}", ERROR)
        sys.exit(1)


@log_function_entry_exit

def execute_commands_in_instance(instance_name):
    """Log in to the WSL instance and execute specified commands."""
    commands = [
    "cd /usr/backend",
    "docker pull arunpragash/angular_todo:1.1",
    '''docker ps --filter "ancestor=arunpragash/angular_todo:1.1" --format '{{.ID}}' | grep -q . || \
(docker ps -a --filter "ancestor=arunpragash/angular_todo:1.1" --filter "status=exited" --format '{{.ID}}' | grep -q . && \
docker ps -a --filter "ancestor=arunpragash/angular_todo:1.1" --filter "status=exited" --format '{{.ID}}' | xargs -r docker start) || \
docker run -d --restart=always -p 9000:80 arunpragash/angular_todo:1.1''',
    "cd /usr/backend && docker compose up --build -d",
    "exit"
]
    wsl_instance = 'cloudbook'
    run_wsl_commands(wsl_instance, commands, "logging_.txt", "infogreen@123")

@log_function_entry_exit
def is_wsl_instance_running(instance_name):
    """Check if a WSL instance is already running."""
    try:
        result = subprocess.run(
            ["wsl", "-l", "--running"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        running_instances = result.stdout
        logging.debug(f"Running WSL instances: {running_instances}")
        update_logs(f"Running WSL instances: {running_instances}", DEBUG)
        return instance_name in running_instances
    except Exception as e:
        logging.error(f"Error checking running WSL instances: {e}")
        update_logs(f"Error checking running WSL instances: {e}", ERROR)
        return False


@log_function_entry_exit
def does_wsl_instance_exist(instance_name):
    """Check if a WSL instance already exists."""
    try:
        result = subprocess.run(
            ["wsl", "-l", "-v"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        existing_instances = result.stdout.strip()
        existing_instances = existing_instances.replace('\x00', '') # parsing into a proper string to make comparision
        logging.debug(f"Existing WSL instances: {existing_instances}")
        update_logs(f"Existing WSL instances: {existing_instances}", DEBUG)
        return (" " +instance_name + " ") in existing_instances # added space to validate exact instance name eg cloudbook not cloudbook1 or 1cloudbook
    except Exception as e:
        logging.error(f"Error checking existing WSL instances: {e}")
        update_logs(f"Error checking existing WSL instances: {e}", DEBUG)
        return False


@log_function_entry_exit
def install_wsl_if_needed():
    """Install WSL if it's not already installed."""
    if not is_wsl_installed():
        logging.info("WSL is not installed. Installing WSL...")
        update_logs("WSL is not installed. Installing WSL...", INFO)
        install_wsl()
    else:
        logging.info("WSL is already installed. Skipping installation.")
        update_logs("WSL is already installed. Skipping installation.", INFO)


@log_function_entry_exit
def import_wsl_instance_if_needed(tar_file, instance_name):
    """Import the WSL instance only if it doesn't already exist."""
    if not does_wsl_instance_exist(instance_name):
        logging.info(f"WSL instance '{instance_name}' does not exist. Importing...")
        update_logs(f"WSL instance '{instance_name}' does not exist. Importing...", INFO)
        import_wsl_instance(tar_file, instance_name)
    else:
        logging.info(f"WSL instance '{instance_name}' already exists. Skipping import.")
        update_logs(f"WSL instance '{instance_name}' already exists. Skipping import.", INFO)


@log_function_entry_exit
def execute_commands_in_instance_if_needed(instance_name):
    """Execute commands in the WSL instance if it's not already running."""
    if not is_wsl_instance_running(instance_name):
        logging.info(f"WSL instance '{instance_name}' is not running. Starting commands...")
        update_logs(f"WSL instance '{instance_name}' is not running. Starting commands...", INFO)
    else:
        logging.info(f"WSL instance '{instance_name}' is already running. Skipping commands.")
        update_logs(f"WSL instance '{instance_name}' is already running. Skipping commands.", INFO)
    execute_commands_in_instance(instance_name)



@log_function_entry_exit
def main():
    configure_logging()
    instance_name = "cloudbook"
    install_wsl_if_needed()
    tar_file = extract_tar_file()
    import_wsl_instance_if_needed(tar_file, instance_name)
    execute_commands_in_instance_if_needed(instance_name)
    start_gui()
    

if __name__ == "__main__":
    main()
