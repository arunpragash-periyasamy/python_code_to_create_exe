import subprocess
def is_wsl_installed():
    try:
        # Check if WSL is present and supports --version (available in WSL 2 and later)
        result = subprocess.run(["wsl", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("WSL is installed.")
        print(f"WSL version output: {result.stdout.decode().strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"WSL version check failed: {e}. Output: {e.stdout.decode()} {e.stderr.decode()}")
    except FileNotFoundError:
        print("WSL is not installed or not available.")
        
    # Fallback check: Test if the `wsl` command exists (for older systems)
    try:
        result = subprocess.run(["wsl", "--help"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("WSL is installed but might not support `--version`.")
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("WSL is not installed or not functional.")
        
        return False
    
print(is_wsl_installed())