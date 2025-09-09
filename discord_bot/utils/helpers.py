def format_message(message: str) -> str:
    """Format a message for display."""
    return message.strip().capitalize()

def is_valid_username(username: str) -> bool:
    """Check if the username is valid."""
    return username.isalnum() and 3 <= len(username) <= 20

def generate_random_id(length: int = 8) -> str:
    """Generate a random alphanumeric ID of specified length."""
    import random
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))