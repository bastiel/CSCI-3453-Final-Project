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
    time.sleep (3)

    new_name = f"{folder_list[0]}_{i}"
    os.rename(folder1, new_name)
    folder1 = new_name
    i += 1
