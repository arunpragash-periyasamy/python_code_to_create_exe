import sys
import os
import shutil
import subprocess
import logging

def get_tar_file_path():
    """Get the path to the embedded tar file."""
    if hasattr(sys, '_MEIPASS'):
        # For PyInstaller bundled executable
        return os.path.join(sys._MEIPASS, "infogreen-billing.tar")
    else:
        # For regular Python script
        return "infogreen-billing.tar"

def extract_tar_file():
    """Extract the embedded tar file to a temporary location."""
    tar_path = get_tar_file_path()
    logging.info(f"Extracting tar file from {tar_path}...")

    # Write the file to a temporary location
    with open(tar_path, "rb") as f:
        tar_data = f.read()
    
    with open("infogreen-billing.tar", "wb") as f:
        f.write(tar_data)
    logging.info(f"Extracted tar file to 'infogreen-billing.tar'")
    return "infogreen-billing.tar"

def is_wsl_installed():
    """Check if WSL is installed."""
    try:
        subprocess.run(["wsl", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        logging.info("WSL is already installed.")
        return True
    except FileNotFoundError:
        logging.info("WSL is not installed.")
        return False

def install_wsl():
    """Install WSL if not already installed."""
    logging.info("Starting WSL installation...")
    try:
        subprocess.run(["wsl", "--install"], check=True)
        logging.info("WSL installation completed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error installing WSL: {e}")
        sys.exit(1)

def import_wsl_instance(tar_file, instance_name):
    """Import the provided tar file into a new WSL instance."""
    if not os.path.exists(tar_file):
        logging.error(f"Error: The file '{tar_file}' does not exist.")
        sys.exit(1)

    logging.info(f"Importing '{tar_file}' as WSL instance '{instance_name}'...")
    try:
        # Ensure the target directory is available and clean
        target_dir = f"C:\\WSL\\{instance_name}"
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
        os.makedirs(target_dir, exist_ok=True)

        # Run the import process and wait for it to finish
        result = subprocess.run(["wsl", "--import", instance_name, target_dir, tar_file], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Log the output from the import process
        logging.info(f"WSL instance '{instance_name}' imported successfully.")
        logging.info("Process completed. Output:\n" + result.stdout.decode())
        if result.stderr:
            logging.error("Errors encountered during import:\n" + result.stderr.decode())

    except subprocess.CalledProcessError as e:
        logging.error(f"Error importing WSL instance: {e}")
        sys.exit(1)

def main():
    instance_name = "testing"

    if not is_wsl_installed():
        install_wsl()

    # Extract the embedded tar file
    tar_file = extract_tar_file()

    import_wsl_instance(tar_file, instance_name)

if __name__ == "__main__":
    main()
