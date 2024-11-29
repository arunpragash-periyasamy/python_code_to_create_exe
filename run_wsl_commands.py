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
                output = f"{command} {result.stdout}"
                error = f"{command} {result.stderr}"
                print(output)
                print(error)
                # Log the results
                log.write(f"Command: {command}\n")
                log.write(f"Output:\n{result.stdout}\n")
                log.write(f"Error (if any):\n{result.stderr}\n")
                log.write("\n" + "-" * 80 + "\n")
    except Exception as e:
        # Catch and log any exceptions
        with open(log_file, 'a', newline='\n') as log:
            log.write(f"An error occurred: {str(e)}\n")
            print(f"An error occurred: {str(e)}\n")







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