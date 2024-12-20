```markdown
# Setup Guide: Install WSL and Configure Docker

## Table of Contents
1. [Install WSL and Configure Ubuntu](#install-wsl-and-configure-ubuntu)
2. [Install Docker in the WSL Instance](#install-docker-in-the-wsl-instance)
3. [Export and Import WSL Instance](#export-and-import-wsl-instance)

---

## Install WSL and Configure Ubuntu

### Steps to Install WSL:
1. Open the Command Prompt:
   - Press `Win` + `R`, type `cmd`, and press Enter.

2. Install WSL:
   ```bash
   wsl --install
   ```
   - This will automatically install WSL and the Ubuntu distribution.
    ![Docker Installation](./screenshots/Screenshot%202024-11-30%20085124.png)
3. Verify the Installation:
   ```bash
   wsl --version
   ```
   ![Docker Installation](./screenshots/Screenshot%202024-11-30%20085304.png)

4. Launch Ubuntu:
   - Run the following command again to open the Ubuntu terminal:
     ```bash
     wsl --install
     ```
   - It will prompt you to create a username and password.
     - Note: While typing the password, no characters will appear, but it is being typed.

5. Once the setup is complete, you will be redirected to the Ubuntu terminal.

---

## Install Docker in the WSL Instance

### Steps to Install Docker:
1. Remove Existing Docker Packages (if any):
   ```bash
   for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
   ```

2. Update and Install Dependencies:
   ```bash
   sudo apt-get update
   sudo apt-get install ca-certificates curl
   ```

3. Add Docker’s Official GPG Key:
   ```bash
   sudo install -m 0755 -d /etc/apt/keyrings
   sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
   sudo chmod a+r /etc/apt/keyrings/docker.asc
   ```

4. Add the Docker Repository:
   ```bash
   echo \
     "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
     $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
     sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   sudo apt-get update
   ```

5. Verify the Docker Installation:
   ```bash
   docker --version
   ```

   Example Output:


---

## Export and Import WSL Instance

### Exporting a WSL Instance:
- To back up your WSL instance, you can export it to a `.tar` file:
  ```bash
  wsl --export <distro-name> <path-to-tar-file>
  ```
  Replace:
  - `<distro-name>`: Name of the WSL instance.
  - `<installation-path>`: Path where you want to install the instance.
  - `<path-to-tar-file>`: Path to the `.tar` file.

  ```bash
  wsl --export Ubuntu C:\Users\Arunpragash\wsl_instance\cloudbook.tar
  ```

### Importing a WSL Instance:
- To restore a WSL instance from a `.tar` file:
  ```bash
  wsl --import <distro-name> <installation-path> <path-to-tar-file>
  ```
  ```bash
  wsl --import cloudbook - C:\Users\Arunpragash\wsl_instance\cloudbook.tar
  ```

---

### Python script for Installing WSL and import our tar:
- install_wsl.py is the final version of the code for converting the exe of tar and executing commands
- Copy the cloudbook.tar and install_wsl3.py in same folder.
- install python and configure the python and pip path in the environment variables
- To make an EXE file we need the pyInstaller, pywin32, PyQT6
 ``` bash
pip install pyinstaller  pywin32 PyQt6
 ```
 - install these packages.
 - command to build the exe of the python and tar
 - If you ico for ICON use it but now it is not working.
 ``` bash
 pyinstaller --onefile --windowed --icon=infogreen.ico --add-data "cloudbook.tar;." --name cloudbook_installer install_wsl3.py
 ```

 - Once the exe is generated then put it in the client system and install it.
## Notes
- Ensure that all commands are executed within the Ubuntu terminal for WSL-related operations.
- For more details or troubleshooting, refer to the official WSL and Docker documentation.
```