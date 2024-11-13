import os
import stat

# Path to the folder in the same directory as the script
folder_path = "./admin_folder"

# Function to set permissions based on user role
def set_permissions_on_login(folder_path, role):
    if role == "admin":
        # Full permissions for owner and group, SGID to ensure group inheritance
        os.chmod(folder_path, stat.S_IRWXU)
    elif role == "normal_user":
        # No permissions for normal users, only owner and group access
        os.chmod(folder_path, stat.S_IRWXU | stat.S_IRGRP)
    else:
        raise ValueError("Unknown role")

# Function to check if the user has access to the folder contents
def access_folder_contents(folder_path, role):
    try:
        # Attempt to list directory contents
        contents = os.listdir(folder_path)
        return f"{role} access granted. Contents: {contents}"
    except PermissionError:
        return f"Permission denied: {role} does not have access to {folder_path}"
    except FileNotFoundError:
        return f"Error: The folder {folder_path} does not exist."

# Simulate a login where permissions are set and access is attempted
def login_user(user_credentials, folder_path):
    # Fetch user role from a database or predefined source
    user_role = get_user_role_from_db(user_credentials)
    
    # Set permissions based on user role
    set_permissions_on_login(folder_path, user_role)
    
    # Attempt to access the folder's contents
    return access_folder_contents(folder_path, user_role)

# Mock database function
def get_user_role_from_db(user_credentials):
    if user_credentials == "admin_user":
        return "admin"
    elif user_credentials == "normal_user":
        return "normal_user"
    else:
        raise ValueError("User not found in database")

# Sample Usage
print(login_user("admin_user", folder_path))    # Admin should have access
print(login_user("normal_user", folder_path))   # Normal user should be denied access