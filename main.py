import os
import signal
import time
import shutil

done = False
i = 0
folder1 = "New Folder"
folder2 = "Second Folder"

### SYS CALL 1 ###
# chunk overwrites folders if already existing
if os.path.exists(folder1):
    shutil.rmtree(folder1)
os.mkdir(folder1)
if os.path.exists(folder2):
    shutil.rmtree(folder2)
os.mkdir(folder2)

## SYS CALL 2 ##
# detects ctrl + c interrupt; deletes created folders and displays message
def signal_handler(signum, frame):
    print("\n\nDeleting newly created folders....")
    time.sleep(2)
    os.rmdir(folder1)
    os.rmdir(folder2)
    print("Finished deleting folders.\nExiting program....\n")
    global done
    done = True

# register interrupt signal
signal.signal(signal.SIGINT, signal_handler)

folder_list= [folder1, folder2]


### SYS CALL 3 AND 4 ###
# Displays the contents of the current directory and renames them every 2 seconds until interrupt is called
print("\nCurrent folders in directory: ")
while not done:
    print(os.listdir('.')) # print current directory
    print("\nRenaming folders... Please wait...\n")
    time.sleep (2) # wait 3 seconds

    if done:
        break

    new_name = f"{folder_list[0]}_{i}" # var holds new name == "New Folder_i" where i++ w/ init of 0
    os.rename(folder1, new_name) # rename folder1 ("New Folder") to new_name ("New Folder_i")
    folder1 = new_name # folder1 originial value is still "New Folder"; must reassign to current name (which is new_name) or else the name won't be found on the next iteration'
    i += 1

    if done:
        break

    new_name = f"{folder_list[1]}_{i}"
    os.rename(folder2, new_name)
    folder2 = new_name

    print("New folder names: ")
