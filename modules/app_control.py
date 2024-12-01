import subprocess  # To execute shell commands
import psutil      # To interact with system processes
import json        # To handle app paths stored in a JSON file
import os          # To verify paths

# Function to load application paths from the JSON file
def load_app_paths():
    """
    Loads application paths from a JSON file.
    Returns:
        dict: A dictionary of application names and paths.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of app_control.py
    config_path = os.path.join(base_dir, "../config/app_paths.json")  # Adjust the relative path
    with open(config_path, "r") as file:
        return json.load(file)

# Load app paths into a global variable for easy access
APP_PATHS = load_app_paths()

def open_application(app_name):
    """
    Opens the application specified by `app_name` using macOS's `open` command.
    Dynamically searches for the app in /Applications.

    Args:
        app_name (str): Name of the application to open.

    Returns:
        str: Success or failure message.
    """
    app_name = app_name.lower().strip()  # Normalize app name
    app_dir = "/Applications"

    # Check if the app is already running
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and app_name in proc.info['name'].lower():
                return f"{app_name.capitalize()} is already open, you dummy"
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    # Search for the application in the /Applications directory
    for app in os.listdir(app_dir):
        if app_name in app.lower() and app.endswith(".app"):
            app_path = os.path.join(app_dir, app)
            try:
                subprocess.Popen(["open", app_path])  # Use `open` for macOS apps
                return f"{app.capitalize()} opened successfully!"
            except Exception as e:
                return f"Failed to open {app.capitalize()}: {str(e)}"

    return f"Application '{app_name}' not found in /Applications."

# Function to close an application
def close_application(app_name):
    """
    Closes the application specified by `app_name` using `psutil` or AppleScript fallback.

    Args:
        app_name (str): Name of the application to close.

    Returns:
        str: Success or failure message.
    """
    app_name = app_name.lower().strip()

    # Try to close using psutil
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and app_name in proc.info['name'].lower():
                proc.terminate()
                proc.wait(timeout=5)
                return f"{app_name.capitalize()} closed successfully!"
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
            pass

    # Fallback to AppleScript if psutil fails
    try:
        subprocess.run(
            ["osascript", "-e", f'tell application "{app_name}" to quit'],
            check=True
        )
        return f"{app_name.capitalize()} closed successfully using AppleScript!"
    except subprocess.CalledProcessError as e:
        return f"Failed to close {app_name.capitalize()} using AppleScript: {str(e)}."

    return f"{app_name.capitalize()} is not currently running."