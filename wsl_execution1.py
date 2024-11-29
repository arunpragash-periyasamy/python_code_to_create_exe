import pexpect

def run_wsl_commands(wsl_instance, wsl_username, commands, password, log_file):
    try:
        with open(log_file, 'w', newline='\n') as log:
            for command in commands:
                # Start a WSL shell
                wsl_command = f"wsl -d {wsl_instance} -u {wsl_username} bash -c \"{command}\""
                log.write(f"Executing: {wsl_command}\n")
                
                # Use pexpect to handle interactive commands
                child = pexpect.spawn(wsl_command, encoding='utf-8')

                # Monitor for password prompt
                try:
                    child.expect(["[Pp]assword:", pexpect.EOF, pexpect.TIMEOUT], timeout=10)
                    if child.before:
                        log.write(child.before + "\n")
                    
                    if "assword" in child.after:
                        child.sendline(password)  # Send password
                        child.expect(pexpect.EOF, timeout=20)  # Wait for command to complete
                except pexpect.TIMEOUT:
                    log.write("Command timed out.\n")
                except pexpect.EOF:
                    pass

                # Write output and errors to log
                log.write(f"Output:\n{child.before}\n")
                child.close()
                log.write("\n" + "-" * 80 + "\n")
    except Exception as e:
        with open(log_file, 'a', newline='\n') as log:
            log.write(f"An error occurred: {str(e)}\n")

# Main script
if __name__ == "__main__":
    # Define WSL instance name
    wsl_instance = "Ubuntu"  # Replace with your WSL instance name
    wsl_username = 'infogreen'
    # Log file path
    log_file = "log.txt"

    # Password for sudo commands
    password = "infogreen"

    # Commands to run
    commands = [
        "docker --help",
        "docker ps",
        "cd /usr && ls"
    ]

    # Run the commands and log the output
    run_wsl_commands(wsl_instance, wsl_username, commands, password, log_file)

    print(f"All commands executed. Output saved in {log_file}")
