import threading
import time
import os
import random

first_install = False

try:
    import psutil
except ImportError:
    # Install psutil using pip
    print("psutil not found, installing...")
    os.system("pip install psutil")
    # Wait a moment to ensure the installation completes
    time.sleep(5)
    # Try importing psutil again
    import psutil
    first_install = True

if first_install:
    print("psutil has been imported successfully!")

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

def get_metrix(start,file):
    """
    This function will grab time, cpu use persentage, memory precentage used, and thread count

    perameters:
    start: the time when get_matrix is called
    file: file that the results will be writen to

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

    content = f"Deration: {duration}\nCPU percentage: {cpu_p}\nMemory percentage: {mem_p.percent}\nNumber of active threads: {thread_c} \n"

    write_to_file(file, content)

def stress_test(path, path_to_file,file, start_thread = 5):
    """
    This function will preform a stress test to see how the system handle more and more thread preforming system calls
    (read, write, create)

    Perameters:
    path: path to the folder used for file createion
    path_to_file: path to a file used for read and write functions
    file: the file the results will be writen to
    start_thread = number of starting threads default 10 
    

    returns: return get metrix function to see how the system handles more and more threads
    """

    tasks = ["write", "read", "create"] #the diffrent tasks the treads can do
    
    #base time for the entire stress test
    start = time.time()

    #get the starting matrix
    print("Base metrix before testing:\n")
    get_metrix(start, file)


    test =True #run untill the thread cound get to 10000
    iteration = 1 
    while test == True:
        #keep track of the time for each threads time
        thread_start = time.time()
        threads = [] #hold all the treads this will reset after each iteration
        for i in range(start_thread):
            task_choose = random.choice(tasks)#randomly choose one task for the thread to preform

            if task_choose == "write":
                #create a tread to write to a file. 
                content = [i for i in range(100)]
                thread = threading.Thread(target=write_to_file, args=(path_to_file,str(content)))
                
                
                
            
            elif task_choose == "read":
                #create a tread to read from a file
                thread = threading.Thread(target=read_file, args = (path_to_file,))
            
                
                
            
            elif task_choose == "create":
                #create a tread to create a file
                file_name = f"new_test_{iteration}_{i}.txt" #this will create multiple unique files
                thread = threading.Thread(target=create_file, args=(path, file_name)) 

            #start the thread and add them to the thread list
            thread.start()
            threads.append(thread)
        
        #join the threads
        for t in threads:
            t.join()
        
        #check metrix after first iteration and places then into the file
        content = f"Iteration: {iteration} with {len(threads)} threads\n"
        write_to_file(file, content)
        get_metrix(thread_start, file)
        

        iteration+=1
        start_thread = start_thread *5
        
        #stop the program after it has reach over 10000 threads created
        if len(threads)>10000:
            test = False
    content = "Stress test finished\nMetrix for entire test\n"
    write_to_file(file, content)
    get_metrix(start,file)
    

if __name__ == "__main__":
    # Path to the folder that will be used to create files
    path = "./stress test"
    
    # Ensure the directory exists
    if not os.path.exists(path):
        os.makedirs(path)

    # Path to the file that will be read and written to 
    path_to_file = os.path.join(path, "astress.txt") 
    if not os.path.exists(path_to_file): 
        with open(path_to_file, 'w') as file: pass # Just create an empty file 
    
    # Path to the result file 
    result_file = os.path.join(path, "aResults.txt") 
    if not os.path.exists(result_file): 
        with open(result_file, 'w') as file: pass # Just create an empty file

    stress_test(path, path_to_file,result_file)
