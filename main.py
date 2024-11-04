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

while not done:
    os.listdir('.')
