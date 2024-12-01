# Utility function to sanitize commands (optional)
def sanitize_command(command):
    """
    Cleans and formats user commands for processing.
    
    Args:
        command (str): The raw command from the user.
    
    Returns:
        str: Sanitized command.
    """
    return command.strip().lower()

# Logging functionality (optional)
def log_event(event):
    """
    Logs events to a file for debugging purposes.
    
    Args:
        event (str): The event description to log.
    """
    with open("jarvis.log", "a") as log_file:
        log_file.write(event + "\n")
