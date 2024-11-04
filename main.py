import os
import signal
import time
import shutil

done = False
i = 0
folder1 = "New Folder"
folder2 = "Second Folder"

# chunk overwrites folders if already existing
if os.path.exists(folder1):
    shutil.rmtree(folder1)
os.mkdir(folder1)
if os.path.exists(folder2):
    shutil.rmtree(folder2)
os.mkdir(folder2)

folder_list= [folder1, folder2]

while not done:
    print(os.listdir('.')) # print current directory
    time.sleep (3) # wait 3 seconds

    new_name = f"{folder_list[0]}_{i}" # var holds new name == "New Folder_i" where i++ w/ init of 0
    os.rename(folder1, new_name) # rename folder1 ("New Folder") to new_name ("New Folder_i")
    folder1 = new_name # folder1 originial value is still "New Folder"; must reassign to current name (which is new_name) or else the name won't be found on the next iteration'
    i += 1

    new_name = f"{folder_list[1]}_{i}"
    os.rename(folder2, new_name)
    folder2 = new_name
