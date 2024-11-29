import subprocess

def run_wsl_commands(wsl_instance, commands, log_file, sudo_password=None):
    try:
        # Prepare the log file
        with open(log_file, 'w', newline='\n') as log:
            # Create a single string of commands
            full_command = " && ".join(commands)
            
            # Check if the command contains sudo and a password is provided
            if sudo_password:
                # Add sudo password handling at the start of the full command
                full_command = f"echo {sudo_password} | sudo -S bash -i -c \"{full_command}\""
            else:
                # Run commands without sudo password handling
                full_command = f"bash -i -c \"{full_command}\""
                
            # Run the WSL command in a single session
            result = subprocess.run(f"wsl -d {wsl_instance} {full_command}", shell=True, text=True, capture_output=True)
            
            # Log the results
            log.write(f"Commands: {commands}\n")
            log.write(f"Output:\n{result.stdout}\n")
            log.write(f"Error (if any):\n{result.stderr}\n")
            log.write("\n" + "-" * 80 + "\n")
    except Exception as e:
        # Catch and log any exceptions
        with open(log_file, 'a', newline='\n') as log:
            log.write(f"An error occurred: {str(e)}\n")

# Main script
if __name__ == "__main__":
    # Define WSL instance name
    wsl_instance = "Ubuntu"  # Replace with your WSL instance name

    # Log file path
    log_file = "log.txt"

    # Commands to run
    commands = [
        "sudo docker --help",
        "sudo docker ps",
        "cd /usr && ls",  # List files in /usr
        "cd src && ls"  # Navigate to /usr/src and list files
    ]

    # Provide the sudo password (if needed)
    sudo_password = "infogreen"  # Replace with your sudo password

    # Run the commands and log the output
    run_wsl_commands(wsl_instance, commands, log_file, sudo_password)

    print(f"All commands executed. Output saved in {log_file}")
