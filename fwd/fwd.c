// clear/set text on screen (/dev/tty1)
// program meant to be setuid root (chown root a.out && chmod 4755 a.out)
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<sys/ioctl.h>
#include<fcntl.h>
#include<unistd.h>

const char USAGE[] = 
"Allow unprivileged users to clear or write error messages to /dev/tty1\n\
Usage:\n\
    ./fwd (-h | --help)     Print this message\n\
    ./fwd 'text'            Clear screen and forward `text` to /dev/tty1\n\
    ./fwd                   Clear screen and center blinking cursor in /dev/tty1";
const char CLEAR[] = "\033c";

// gen newlines/spaces to put cursor in center of screen
// does NOT contain CLEAR string
// NOTE needs to be freed
char* reset_buffer(int dst_tty)
{
    struct winsize ws;
    if (ioctl(dst_tty, TIOCGWINSZ, &ws) != 0) {
        perror("Failed to get /dev/tty1 size");
        exit(3);
    }
    int width = ws.ws_col / 2 - 1;
    int height = ws.ws_row / 2 - 1;
    size_t buf_len = width + height + 1;
    char* buffer = (char*)calloc(1, buf_len);
    buffer[buf_len] = '\0';
    memset(buffer, '\n', height);
    memset(buffer+height, ' ', width);
    return buffer;
}

int main(int argc, char* argv[])
{
    int help = argc == 2 && (!strcmp(argv[1], "-h") || !strcmp(argv[1], "--help"));
    if (argc > 2 || help) {
        puts(USAGE);
        return EXIT_FAILURE;
    }

    // open tty
    int fd = open("/dev/tty1", O_RDWR);
    if (fd == -1) {
        perror("Failed to open /dev/tty1 (are you root?)");
        exit(2);
    }

    // get text
    char* text = NULL;
    int free_buffer = 0;
    if (argc == 2) {
        text = argv[1];
    } else {
        text = reset_buffer(fd);
        free_buffer = 1;
    }

    // prepend CLEAR
    size_t clear_len = strlen(CLEAR);
    size_t text_len = strlen(text);
    int buf_len = clear_len + text_len;
    char* buffer = (char*)calloc(1, buf_len);
    strncpy(buffer, CLEAR, clear_len);
    strncpy(buffer+clear_len, text, text_len);
    buffer[buf_len] = '\0';

    // write
    int rc = write(fd, buffer, buf_len);
    if (rc < buf_len && rc > 0) {
        printf("Only wrote %d bytes out of %d\n", rc, buf_len);
    } else if (rc == -1) {
        perror("Failed to write");
    }

    free(buffer);
    if (free_buffer == 1) {
        free(text);
    }

    return EXIT_SUCCESS;
}
