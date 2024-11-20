#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include <unistd.h>
#include <errno.h>
#include <sys/types.h>

#define MAX_PATH_LEN 256

// Function to list files in a directory
void list_files(const char *path) {
    DIR *dp = opendir(path);
    if (!dp) {
        perror("opendir");
        return;
    }

    printf("Contents of %s:\n", path);
    struct dirent *entry;
    while ((entry = readdir(dp)) != NULL) {
        printf("%s\n", entry->d_name);
    }

    closedir(dp);
}

// Function to create a new file
void create_file(const char *path) {
    FILE *file = fopen(path, "w");
    if (!file) {
        perror("fopen");
        return;
    }
    printf("File created: %s\n", path);
    fclose(file);
}

// Function to create a new directory
void create_directory(const char *path) {
    if (mkdir(path, 0755) == -1) {
        perror("mkdir");
        return;
    }
    printf("Directory created: %s\n", path);
}

// Function to delete a file or directory
void delete_file_or_directory(const char *path) {
    if (remove(path) == -1) {
        perror("remove");
        return;
    }
    printf("Deleted: %s\n", path);
}

// Function to view permissions of a file or directory
void view_permissions(const char *path) {
    struct stat fileStat;
    if (stat(path, &fileStat) == -1) {
        perror("stat");
        return;
    }

    printf("Permissions for %s: ", path);
    printf((S_ISDIR(fileStat.st_mode)) ? "d" : "-");
    printf((fileStat.st_mode & S_IRUSR) ? "r" : "-");
    printf((fileStat.st_mode & S_IWUSR) ? "w" : "-");
    printf((fileStat.st_mode & S_IXUSR) ? "x" : "-");
    printf((fileStat.st_mode & S_IRGRP) ? "r" : "-");
    printf((fileStat.st_mode & S_IWGRP) ? "w" : "-");
    printf((fileStat.st_mode & S_IXGRP) ? "x" : "-");
    printf((fileStat.st_mode & S_IROTH) ? "r" : "-");
    printf((fileStat.st_mode & S_IWOTH) ? "w" : "-");
    printf((fileStat.st_mode & S_IXOTH) ? "x" : "-");
    printf("\n");
}

// Function to change permissions of a file or directory
void change_permissions(const char *path, mode_t mode) {
    if (chmod(path, mode) == -1) {
        perror("chmod");
        return;
    }
    printf("Permissions changed for %s\n", path);
}

// Function to open the text file externally using a text editor (e.g., nano, vim)
void open_file(const char *path) {
    char command[512];

    snprintf(command, sizeof(command), "xdg-open %s", path); // For Linux systems

    int ret = system(command);
    if (ret != 0) {
        perror("Error opening file externally");
    }
}

// Function to handle command input and execute corresponding functions
void execute_command(char *command) {
    char path[MAX_PATH_LEN];
    char cmd[50];
    mode_t mode;

    if (sscanf(command, "%s %s", cmd, path) < 1) {
        printf("Invalid command format.\n");
        return;
    }

    if (strcmp(cmd, "list") == 0) {
        list_files(path);
    } else if (strcmp(cmd, "create_file") == 0) {
        create_file(path);
    } else if (strcmp(cmd, "create_dir") == 0) {
        create_directory(path);
    } else if (strcmp(cmd, "delete") == 0) {
        delete_file_or_directory(path);
    }
    else if (strcmp(cmd, "open") == 0) {
        open_file(path);
    } else if (strcmp(cmd, "view_permissions") == 0) {
        view_permissions(path);
    } else if (strcmp(cmd, "change_permissions") == 0) {
        if (sscanf(command, "change_permissions %s %o", path, &mode) == 2) {
            change_permissions(path, mode);
        } else {
            printf("Invalid permission format. Example: 0644\n");
        }
    } else {
        printf("Unknown command: %s\n", cmd);
    }
}

int main() {
    char command[512];

    printf("Welcome to the Bootleg File Explorer!\n");

    while (1) {
        printf("\nCommands:\n");
        printf("1. list [path]\n");
        printf("2. create_file [path]\n");
        printf("3. create_dir [path]\n");
        printf("4. delete [path]\n");
        printf("5. open [path]\n");
        printf("5. view_permissions [path]\n");
        printf("6. change_permissions [path] [mode (e.g., 0644)]\n");
        printf("7. exit\n");
        printf("> ");
        
        if (!fgets(command, sizeof(command), stdin)) {
            break;
        }

        command[strcspn(command, "\n")] = '\0';

        if (strcmp(command, "exit") == 0) {
            break;
        }

        execute_command(command);
    }

    return 0;
}