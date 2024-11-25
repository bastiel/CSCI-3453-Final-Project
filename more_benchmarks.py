import os
import time
import threading
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
def list_directory(path):
    """
    List all contents of a directory using system calls.

    Parameters:
    path: The directory path to list contents.

    Return: None, but prints the contents.
    """
    try:
        #List directory contents
        contents = os.listdir(path)
        print(f"Contents of {path}: {contents}")
    except OSError as e:
        print(f"Error listing directory {path}: {e}")

def change_directory(path):
    """
    Change the current working directory using system calls.

    Parameters:
    path: The directory path to change to.

    Return: None, but prints the current directory.
    """
    try:
        #Change to the specified directory
        os.chdir(path)
        print(f"Changed to directory: {os.getcwd()}")
    except OSError as e:
        print(f"Error changing directory to {path}: {e}")

def create_process():
    """
    Create a new process using system calls and print its PID.

    Return: None, but prints the PID.
    """
    try:
        pid = os.fork()  #Works only on Unix-based systems
        if pid == 0:
            print(f"Child process created with PID: {os.getpid()}")
            os._exit(0)  #Ensure child exits after creation
        else:
            os.wait()  #Wait for the child process to finish
    except AttributeError:
        print("os.fork is not available on this system.")
    except OSError as e:
        print(f"Error creating process: {e}")

def get_process_info():
    """
    Retrieve and print the current process info using psutil.

    Return: None, but prints the process details.
    """
    try:
        process = psutil.Process(os.getpid())
        print(f"Process ID: {process.pid}, Name: {process.name()}, Status: {process.status()}")
    except psutil.Error as e:
        print(f"Error retrieving process information: {e}")

def get_metrics(start, file):
    """
    Gather and log metrics: time, CPU usage, memory usage, and active threads.

    Parameters:
    start: The start time of the benchmark.
    file: File to log metrics.

    Return: None
    """
    duration = time.time() - start
    cpu_p = psutil.cpu_percent(interval=None)
    mem_p = psutil.virtual_memory()
    thread_c = threading.active_count()

    content = f"Duration: {duration}\nCPU percentage: {cpu_p}\nMemory percentage: {mem_p.percent}\nActive threads: {thread_c}\n\n"
    write_to_file(file, content)

def write_to_file(path, content):
    """
    Write content to a file using system calls.

    Parameters:
    path: Path to the file.
    content: Content to write.

    Return: None
    """
    try:
        file = os.open(path, os.O_WRONLY | os.O_APPEND)
        os.write(file, content.encode())
        os.close(file)
    except OSError as e:
        print(f"Error writing to the file {path}: {e}")

def time_test(path, results_file, num_threads=50):
    """
    Perform benchmarks for file system navigation and process management with multiple threads.

    Parameters:
    path: Directory path for tests.
    results_file: File to log metrics.
    num_threads: Number of threads for testing (default: 50).

    Return: None
    """
    tasks = ["list", "change_dir", "create_process", "get_process_info"]
    threads = []
    start = time.time()

    write_to_file(results_file, "Base metrics:\n")
    get_metrics(start, results_file)

    for i in range(num_threads):
        task_choice = random.choice(tasks)
        function_name = ""

        if task_choice == "list":
            thread = threading.Thread(target=list_directory, args=(path,))
            function_name = "list_directory"
        elif task_choice == "change_dir":
            thread = threading.Thread(target=change_directory, args=(path,))
            function_name = "change_directory"
        elif task_choice == "create_process":
            thread = threading.Thread(target=create_process)
            function_name = "create_process"
        elif task_choice == "get_process_info":
            thread = threading.Thread(target=get_process_info)
            function_name = "get_process_info"

        threads.append(thread)
        thread.start()

        #Log function being called
        content = f"At thread {i + 1}, function: {function_name}\n"
        write_to_file(results_file, content)

        #Log metrics
        get_metrics(start, results_file)

    for t in threads:
        t.join()

    write_to_file(results_file, "Benchmark test complete.\n")
    get_metrics(start, results_file)


if __name__ == "__main__":
    path = "/home/ubuntu/benchmark test"
    results_file = "/home/ubuntu/benchmark test/results"
    
    #Run benchmark test
    time_test(path, results_file)