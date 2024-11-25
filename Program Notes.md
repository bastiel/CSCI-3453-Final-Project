# OS System Call-Thread Performance Project Notes 

## Problem Statement
### How do we monitor hardware resources usage (such as: number of active threads, CPU percentage, memory percentage, task duration) while tasks are being performed using system calls? 
---
## Program Overview
1. Each execution, the program will create a new folder to hold the test files and results
2. There will be 3 tasks that will be randomly chosen to execute (done with system calls via Python's `os` library) on random test files: 
    - Creating files
    - writing to files
    - reading the files
3. Each test monitors a thread during task exe and measure the following metrics:
    - Time duration per test 
    - CPU percentage per test 
    - Memory percentage per test 
    - Number of active threads per test
4. The metrics will be output and formatted onto a file
---
## Functions for System Calls 
### `write_to_file` - writes content to a file using system calls
- Parameters:
    - `path`: The path to the file
    - `content`: a string that will be writen to the folder
    - `return`: content written to the file
### `read_file` - read content from the from a file
- Parameters
    - `path` - path to the file being read 
    - `return` - content from the file 
