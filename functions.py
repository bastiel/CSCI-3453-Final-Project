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

def check_permission(user,actions, action):#not needed if doing on vertual machine
    """
    This function will simulate the permission error used with user and groups

    Perameters:
    user: user trying to do something
    action: list of actions the user can do
    action: what the user is trying to do

    return: error raised if they user cant preform the action 
    """
    print(actions)
    if action not in actions:
        print(f"{action} not found")
        raise PermissionError(f"{user} does not have permission to {action}")
    
def write_to_file(path, content):
    """
    This function will write content to a file useing system calls

    Perameters:
    path: The path to the file
    content: a string that will be writen to the folder

    return: content written to the file
    """
    #try to find the file to write
    try:
        #this will open the file with the path with write and read or append functionality
        file = os.write(path, os.O_WRONLY | os.O_APPEND)
        #actually writes the content to the file
        os.write(file, content.encode())
        #close the file
        os.close(file)
        print(f"Writting to {path} was successfull")
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

def create_folder(path, folder_name):
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
        os.mkdir(path)
        print(f"{folder_name} has been created successfully")
    except FileExistsError:
        print(f"path not found. {folder_name} not created.")
    except OSError as e:
        print(f"Expected error in creating a folder/file: {e}")

def rename_file(old, new):
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
        
        os.rename(old, new)
        print(f"File renamed from {old} to {new}")
    except FileNotFoundError:
        print(f"{old} file not found")
    
    except OSError as e:
        print(f"Error in renameing file {old}: {e}")

def delete_file(path):
    """
    This function will delete a file using system calls

    Perameters:
    user: user tring to delete the file
    path: path to the file
    
    return: delete a file
    """
    try:
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
        print(contents)
        return
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

def Create_txt_file(path, name):
    """
    This function will create a text file with a folder

    Perameters:
    path: path to the folder
    name: txt file name

    return: creates a txt file
    """
    file_path = os.path.join(path, name)

    try:
        os.makedirs(path, exist_ok =True)
        file = os.open(file_path, os.O_CREAT | os.O_RDWR | os.O_TRUNC)
        os.close(file)
        print(f"file {name} successfully created")
    except FileNotFoundError:
        print("folder not found")
    except OSError as e:
        print(f"Error occured: {e}")

if __name__ == "__main__":
    #sets the permissions for each user
    user_name = ["Tcresswell", "Nvu", "AZadron", "AVanbaelinghem", "Lsoundarya"]
    passwords = ["Password123", "Password124", "Password125", "Password126","Password127"]
    admin = ["1",'2','3', '2','3']

    permissions = {1:"admin,create,rename,write,read,", 2:"rename,write,read",3:"read"}

    comp_df = create_df(user_name,passwords,admin)
    log_in = True
    while log_in:
        try:
            
            user = input("Enter user name: ")
            password = input("Enter password: ")

            user_row = comp_df[comp_df["User Name"] == user]
        
            if user_row.empty:
                raise ValueError("Username or password not found")
            if user_row['Passwords'].iloc[0] !=password:
                raise ValueError("Username or password not found")
            os.system("cls")
            log_in = False
        except ValueError as ve:
            os.system("cls")
            print(f"Error {ve}")
        except Exception as e:
            os.system("cls")
            print(f"Unexpected error occured {e}")

    #get the group id and the tast the user can do
    group_id = user_row["Group"].iloc[0]
    roles = permissions.get(int(group_id)).split(",") #list of all the roles the user can do
    
    menu = True
    path = "C:\\Users\\SPeCS\\OneDrive\\Documents\\OS system call project\\workflow"
    while menu:
        
        print(f"welcome {user}",
              "\n1) View directory",
              "\n2) View users",
              "\n3) Done")
        try:
            
            choose = input("Choose option: ")


            if choose == "1":
                #view directory
                choose_1_menu = True
                while choose_1_menu:
                    os.system("cls")
                    list_dir(path)
                    print("1) add folder",
                        "\n2) add file",
                        "\n3) Rename file",
                        "\n4) Read file",
                        "\n5) Delete file",
                        "\n5) Done")
                    choose1 = input("What would you like to do: ")
                    if choose1 == '1':
                        #add folder
                        os.system("cls")
                        check_permission(user, roles,"create")
                        folder_name = input("What is the name of the folder: ")
                        path_to_folder = os.path.join(path, folder_name)
                        create_folder(path_to_folder, folder_name)
                    
                    elif choose1 == '2':
                        #add file
                        folder_name = input("What folder do you want to add to. Press enter if current folder: ")

                        
                        if folder_name == "":
                            check_permission(user, roles, "create")
                            file_name = input("Name of the file: ") + ".txt"
                            Create_txt_file(path, file_name)
                            input("press and key to continue------->")
                        else:
                            check_permission(user, roles, "create")
                            file_name = input("Name of the file: ") + ".txt"
                            new_path = path+"\\"+folder_name
                            create_folder(new_path,file_name)
                            input("press enter to continue-------->")

                    elif choose1 == '3':
                        #Rename file
                        old = input("What file/folder do you want to rename: ")
                        new = input("What new name for the file/folder: ")
                        old_path = os.path.join()
                        rename_file(old,new)
                        
        except ValueError:
            os.system("cls")
            print(f"{choose} not a valid entry")

        except PermissionError as pe:
            print(str(pe))

        

        
    