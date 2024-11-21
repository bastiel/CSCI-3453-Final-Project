import threading
import time
import os
import psutil
import random

##FUNCTIONS FOR SYSTEM CALLS##
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
        file = os.open(path, os.O_WRONLY | os.O_APPEND)
        #actually writes the content to the file
        os.write(file, content.encode()) # write requires a file that has been opened and they bytes of the content (content.encode())
        #close the file
        os.close(file)
        print("Write successfull")
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
        print("file read successfully")
    except OSError as e:
        print(f"Could not read file in {path}: {e}")


def create_file(path, file):
    """
    This function will create a txt file using system calls

    perameters:
    path: the path to where the file will be created
    file: the name of the file to be created

    return: creates a new txt file
    """
    #creates the full path to the file
    path_to_file = os.path.join(path, file)

    try:
        #create the file
        file = os.open(path_to_file, os.O_CREAT | os.O_RDWR | os.O_TRUNC) # creates the file to be able to read and write and will be truckated if the file already exist

        #close the file after creating
        os.close(file)
        print("file created")
    except OSError as e:
        print(f"Error: {e}")

def get_metrix(start):
    """
    This function will grab time, cpu use persentage, memory precentage used, and thread count

    perameters:
    start: the time when get_matrix is called

    return: will print the matrix listed above

    reference:
    https://psutil.readthedocs.io/en/latest/
    """
    #how much time has passed
    duration = time.time()-start
    #precentage of the cpu in use since last call
    cpu_p = psutil.cpu_percent(interval =None) 
    #percent of memory being used
    mem_p = psutil.virtual_memory()
    #tread counts
    thread_c = threading.active_count()

    #display the metrix
    print(f"Deration: {duration}\nCPU percentage: {cpu_p}\nMemory precentage: {mem_p.percent}\nNumber of active threads: {thread_c} ")

def time_test(path,path_to_file, num_treads=50, run_time = 15):
    """
    This function will test the system with handleing 50 threads preforming random file system calls (write, read, create)

    Perameter:
    path: the path to the folder used for file creation
    path_to_file: used for reading and writing to a test file
    num_treads: number of threads to be created- default=50
    time: The time the threads will be running- default = 15 seconds

    return: multiple metrix using psutil
    """

    tasks = ["write", "read", "create"] #the diffrent tasks the treads can do
    threads = [] #hold all the treads
    start = time.time()
    get_metrix(start)
    
    for i in range(num_treads): #create num_treads(default = 50) of treads
        #randomly choose a task to do and choose a random file to do it on
        task_choose = random.choice(tasks)

        if task_choose == "write":
            #create a tread to write to a file. 
            content = [i for i in range(100)]
            thread = threading.Thread(target=write_to_file, args=(path_to_file,str(content)))
                
                
                
            
        elif task_choose == "read":
            #create a tread to read from a file
            thread = threading.Thread(target=read_file, args = (path_to_file,))
            
                
                
            
        elif task_choose == "create":
            #create a tread to create a file
            file_name = f"new_test_{i}.txt" #this will create multiple unique files
            thread = threading.Thread(target=create_file, args=(path, file_name))
                
        threads.append(thread)
        thread.start()

        get_metrix(start)#periodicly get the metrix for the time test
        time.sleep(1)#pause to simulate actual thread creation
    
    #join the threads to finish the tasks
    for t in threads:
        t.join()
        
    print("The time test is complete")
    get_metrix(start)     

if __name__ == "__main__":
    path = "C:\\Users\\SPeCS\\OneDrive\Documents\\OS system call project\\benchmark test"
    path_to_file = "C:\\Users\\SPeCS\\OneDrive\\Documents\\OS system call project\\benchmark test\\benchmark_test.txt"

    ##RUN TIMED TEST FOR 50 THREADS##
    time_test(path,path_to_file)
            



