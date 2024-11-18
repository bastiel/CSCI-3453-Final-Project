import os
import pandas as pd

def create_df(usernames, passwords, groups):
    """
    This function will create a dataframe of the users password and group they belong to 

    Perameters:
    usernames: List of the user names for the employees
    passwords: list of the passwords for the emeployees
    groups: 1(admin),2(editor),3(viewer)

    returns: A datafram of the employees
    """
    data = {"User Name": usernames, "Passwords":passwords, "Group": groups}
    df = pd.DataFrame(data)

    return df

def check_permission(user, action):#not needed if doing on vertual machine
    """
    This function will simulate the permission error used with user and groups

    Perameters:
    user: user trying to do something
    action: the action the user would like to preform

    return: error raised if they user cant preform the action 
    """
    permissions = user['permissions']
    if action not in permissions:
        raise PermissionError(f"{user['user_name']} does not have permission to do {action}")
    
def write_to_file(user,path, content):
    """
    This function will write content to a file useing system calls

    Perameters:
    path: The path to the file
    content: a string that will be writen to the folder

    return: content written to the file
    """
    #try to find the file to write
    try:
        #check if the user can write to the file
        check_permission(user, "write")
        #this will open the file with the path with write and read or append functionality
        file = os.write(path, os.O_WRONLY | os.O_APPEND)
        #actually writes the content to the file
        os.write(file, content.encode())
        #close the file
        os.close(file)
        print(f"Writting to {path} was successfull")
    except PermissionError as pe:
        print(str(pe))
    except OSError as e:
        print(f"Error in writing to the file: {e}")

def read_file(path):
    """
    This function will alow the user to read from the from a folder

    Perameters:
    path: path to the file to read

    return the content from the file
    """
    try:
        #open file with read only enabled in read only
        file = os.open(path, os.O_RDONLY)
        content = os.read(file, 1024)
        os.close(file)
        print(f"{content}")
    except OSError as e:
        print(f"Could not read file in {path}: {e}")

def create_folder(user, path, folder_name):
    """
    This Function will create a folder

    Perameters:
    user: user trying to create folder
    path: path to the folder
    folder_name: name of the folder

    return: folder created
    """
    
    #try to create a folder and if the path doesnt exest it will cause and error
    try:
        check_permission(user, "create")
        os.mkdir(path+folder_name)
        print(f"{folder_name} has been created successfully")
    except PermissionError as pe:
        print(str(pe))
    except FileExistsError:
        print(f"path not found. {folder_name} not created.")
    except OSError as e:
        print(f"Expected error in creating a folder: {e}")

def rename_file(user,old, new):
    """
    This function will rename a file using system calls

    Perameters:
    user: the user that is tring to rename the filed
    old: old name
    new: new name

    return: file renamed
    """
    #try to rename a file and if old file not found it will pull an error
    try:
        check_permission(user, 'write')
        os.rename(old, new)
        print(f"File renamed from {old} to {new}")
    except FileNotFoundError:
        print(f"{old} file not found")
    except PermissionError as pe:
        print(str(pe))
    except OSError as e:
        print(f"Error in renameing file {old}: {e}")

def delete_file(user,path):
    """
    This function will delete a file using system calls

    Perameters:
    user: user tring to delete the file
    path: path to the file
    
    return: delete a file
    """
    try:
        check_permission(user, "delete")
        os.remove(path)
        print(f"file in {path} deleted.")
    except OSError as e:
        print(f"Error deleting file in {path}: {e}")

def list_dir(path):
    """
    This function will list the folders in a directory

    Perameters:
    path: path to the directory

    return: returns folders in directory
    """
    try:
        contents = os.listdir(path)
        return contents
    except FileNotFoundError:
        return f"{path} not found."
    except PermissionError:
        return f"You do not have permission to access {path}"

def move(user, curr_path, next_path):
    """
    This function will move a folder from one directory to another directory

    Perameters:
    user: user trying to do the task
    curr_path: current path to the folder
    next_path: path the the location where the file will be

    return: string on if the function was successful
    """
    