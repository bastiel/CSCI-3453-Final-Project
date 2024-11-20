#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include <unistd.h>
#include <errno.h>
#include <sys/types.h>


void list_files(const char *path) {
    struct dirent *entry;
    DIR *dp = opendir(path);

    if (dp == NULL) {
        perror("opendir");
        return;
    }

    printf("Contents of %s:\n", path);
    while ((entry = readdir(dp)) != NULL) {
        printf("%s\n", entry->d_name);
    }

    closedir(dp);
}

void create_file(const char *path) {
    FILE *file = fopen(path, "w");
    if (file == NULL) {
        perror("fopen");
        return;
    }
    printf("File created: %s\n", path);
    fclose(file);
}

void create_directory(const char *path) {
    if (mkdir(path, 0755) == -1) {
        perror("mkdir");
        return;
    }
    printf("Directory created: %s\n", path);
}

void delete_file_or_directory(const char *path) {
    if (remove(path) == 0) {
        printf("Deleted: %s\n", path);
    } else {
        perror("remove");
    }
}

void view_permissions(const char *path) {
    struct stat fileStat;
    if (stat(path, &fileStat) < 0) {
        perror("stat");
        return;
    }

    printf("Permissions for %s:\n", path);
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

void change_permissions(const char *path, mode_t mode) {
    if (chmod(path, mode) == -1) {
        perror("chmod");
        return;
    }
    printf("Permissions changed for %s\n", path);
}

int main() {
    char command[256];
    char path[256];
    char base_path[256] = ".";
    mode_t mode;

    printf("Welcome to the Bootleg File Explorer!\n");

    while (1) {
        printf("\nCommands:\n");
        printf("1. list [path]\n");
        printf("2. create_file [path]\n");
        printf("3. create_dir [path]\n");
        printf("4. delete [path]\n");
        printf("5. view_permissions [path]\n");
        printf("6. change_permissions [path] [mode (e.g., 0644)]\n");
        printf("7. exit\n");
        printf("> ");

        fgets(command, sizeof(command), stdin);
        command[strcspn(command, "\n")] = '\0'; // Remove newline

        if (strncmp(command, "list", 4) == 0) {
            sscanf(command, "list %s", path);
            list_files(path);
        } else if (strncmp(command, "create_file", 11) == 0) {
            sscanf(command, "create_file %s", path);
            create_file(path);
        } else if (strncmp(command, "create_dir", 10) == 0) {
            sscanf(command, "create_dir %s", path);
            create_directory(path);
        } else if (strncmp(command, "delete", 6) == 0) {
            sscanf(command, "delete %s", path);
            delete_file_or_directory(path);
        } else if (strncmp(command, "view_permissions", 17) == 0) {
            sscanf(command, "view_permissions %s", path);
            view_permissions(path);
        } else if (strncmp(command, "change_permissions", 19) == 0) {
            sscanf(command, "change_permissions %s %o", path, &mode);
            change_permissions(path, mode);
        } else if (strcmp(command, "exit") == 0) {
            break;
        } else {
            printf("Unknown command.\n");
        }
    }

    return 0;
}