import os
import signal
import time
import shutil

done = False
i = 0
new_dir = "New Folder"
new_dir2 = "Second Folder"

if os.path.exists(new_dir):
    shutil.rmtree(new_dir)
os.mkdir(new_dir)
if os.path.exists(new_dir2):
    shutil.rmtree(new_dir2)
os.mkdir(new_dir2)
import os
import signal
import time
import shutil

done = False
i = 0
new_dir = "New Folder"
new_dir2 = "Second Folder"

# chunk overwrites folders if already existing
if os.path.exists(new_dir):
    shutil.rmtree(new_dir)
os.mkdir(new_dir)
if os.path.exists(new_dir2):
    shutil.rmtree(new_dir2)
os.mkdir(new_dir2)

print(os.listdir('.')) # print current directory
time.sleep (3)
new_dir = os.rename(new_dir, "hello") # rename new_dir to "hello"
print(os.listdir('.')) # print current direc again


'''
while not done:
    print(list_directory)
    os.rename(new_dir, (new_dir + "_" + str(i)))
    i += 1

    os.rename (new_dir2, (new_dir2 + "_" + str(i)))
    i+=1

    time.sleep(5)
    print(list_directory)
'''
