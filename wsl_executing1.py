import subprocess

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
                
                # Log the results
                log.write(f"Command: {command}\n")
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
        # "sudo apt-get update",
        # "sudo apt-get upgrade -y",
        "sudo docker --help",
        "sudo docker ps",
        "cd /usr && ls"
    ]

    # Provide the sudo password (if needed)
    sudo_password = "infogreen"  # Replace with your sudo password

    # Run the commands and log the output
    run_wsl_commands(wsl_instance, commands, log_file, sudo_password)

    print(f"All commands executed. Output saved in {log_file}")
