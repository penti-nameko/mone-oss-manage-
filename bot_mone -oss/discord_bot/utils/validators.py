def is_valid_email(email):
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_username(username):
    return username.isalnum() and 3 <= len(username) <= 20

def is_valid_password(password):
    return len(password) >= 8 and any(char.isdigit() for char in password) and any(char.isalpha() for char in password)

def is_valid_guild_id(guild_id):
    return isinstance(guild_id, int) and guild_id > 0

def is_valid_channel_id(channel_id):
    return isinstance(channel_id, int) and channel_id > 0