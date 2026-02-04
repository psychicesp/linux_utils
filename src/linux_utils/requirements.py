import subprocess
import shutil
import functools
import sys

# Centralized list of system command dependencies
DEPENDS = {"tree"}

def ensure_dependencies():
    """Iterates through a list of system commands and offers to install missing ones."""
    missing = [d for d in DEPENDS if not shutil.which(d)]
    
    if not missing:
        return True

    print(f"[-] Missing system requirements: {', '.join(missing)}")
    choice = input("Would you like to attempt to install them? (requires sudo) [y/N]: ").lower()
    
    if choice != 'y':
        return False

    # Detect Package Manager
    if shutil.which("apt"):
        install_cmd = ["sudo", "apt", "install", "-y"]
    elif shutil.which("dnf"):
        install_cmd = ["sudo", "dnf", "install", "-y"]
    elif shutil.which("pacman"):
        install_cmd = ["sudo", "pacman", "-S", "--noconfirm"]
    else:
        print("No supported package manager found. Please install manually.")
        return False

    try:
        print(f"Installing: {missing}...")
        subprocess.run(install_cmd + missing, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Installation failed: {e}")
        return False

def auto_setup(func):
    """
    Decorator that tries to run a function. If it fails due to a 
    missing system binary, it attempts to fix the environment and retries.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (FileNotFoundError, subprocess.CalledProcessError):
            if ensure_dependencies():
                print("Environment repaired. Retrying...")
                return func(*args, **kwargs)
            else:
                print("Requirement check failed. Aborting.")
                sys.exit(1)
    return wrapper