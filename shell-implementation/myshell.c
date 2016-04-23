/*
 * myshell.c
 * Author: Alex LaFroscia
 * Date:   Nov 28, 2014
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <sys/times.h>

#define INPUT_LENGTH 256
#define TRUE 1
#define FALSE 0

// Global variables
char sep[] = " ()<>|&;\n\t";

typedef struct redirect_files {
  char *in;
  char *out;
} redirect_files;

// Function Prototypes
void execute(char *, int, redirect_files *);
void get_redirects(char *, redirect_files *);

/*
 * Main
 */
int main() {
  int status;
  char *input              = malloc(sizeof(char) * INPUT_LENGTH);
  char *check_first_token  = malloc(sizeof(char) * INPUT_LENGTH);
  redirect_files *files;
  char *token;

  // Forever loop
  while(1) {
    files = malloc(sizeof(redirect_files));
    memset(files, 0, sizeof(redirect_files));

    printf("$ ");
    fgets(input, INPUT_LENGTH, stdin);

    // Get the redirect files (for in and output) and put the file names
    // into the "files" struct.  Also, strip the redirections out of the
    // command input
    get_redirects(input, files);

    // Tokenize the string
    // A copy needs to be made because tokenization seems
    // to make changes to the original string
    strcpy(check_first_token, input);

    token = strtok(check_first_token, sep);

    if(strcmp(token, "exit") == 0) {
      // Handle exit
      exit(0);
    } else if(strcmp(token, "cd") == 0) {
      // Handle cd
      token = strtok(NULL, sep);
      status = chdir(token);
    } else if(strcmp(token, "time") == 0) {
      input = input + sizeof(char) * 5;
      execute(input, TRUE, files);
    } else {
      execute(input, FALSE, files);
    }

    // Free files struct
    free(files);

  } // End of while loop

  free(check_first_token);
  free(input);

} // End of main


/*
 * Execute
 *
 * Execute a different program in the current process
 */
void execute(char *input, int time, redirect_files *files) {
  pid_t  pid;
  int    status = 0;
  int    error = 0;
  int    num_token_items = 0;
  char   *token = strtok(input, sep);
  char   **token_list = NULL;
  struct tms *times_struct = malloc(sizeof(struct tms));
  static clock_t cu_time = 0;
  static clock_t cs_time = 0;


  // Get the tokenized version of the input
  while(token != NULL) {
    token_list = realloc(token_list, sizeof(char*) * ++num_token_items);
    if (token_list == NULL) {
      printf("error allocating memory, exiting\n");
      exit(-1);
    }
    token_list[num_token_items - 1] = token;
    token = strtok(NULL, sep);
  }

  token_list = realloc(token_list, sizeof(char*) * ++num_token_items);
  token_list[num_token_items - 1] = NULL;

  if ((pid = fork()) < 0) {               // There was an error while forking
    printf("There was an error while forking!\n");
    exit(1);
  } else if (pid == 0) {                  // This process is the child

    if (files->out != NULL) {
      if (freopen(files->out, "w+", stdout) == NULL) {
        printf("ERROR: %s\n", strerror(errno));
        exit(error);
      }
    }
    if (files->in != NULL) {
      if (freopen(files->in, "r+", stdin) == NULL) {
        printf("ERROR: %s\n", strerror(errno));
        exit(error);
      }
    }

    if ((error = execvp(*token_list, token_list)) < 0) {
      printf("ERROR: %s\n", strerror(errno));
      exit(error);
    }

    // Clean up after opening files
    if (files->out != NULL) {
      fclose(stdout);
    }
    if (files->in != NULL) {
      fclose(stdin);
    }

  } else {                                // This process is the parent
    // Wait until the child is done
    while( wait(&status) != pid)
      ;

    // Print out message about completion state
    if (status != 0) {
      printf("ERROR: Status code %d\n", status);
    }
  }

  // Get times
  times(times_struct);
  if (time == TRUE) {
    // If the first option is "times" then print them
    // Note, the child time is cumulative so we need to do some math
    printf("User:   %lu ticks\n", times_struct->tms_cutime - cu_time);
    printf("System: %lu ticks\n", times_struct->tms_cstime - cs_time);
  }
  // Keep track of the current cumulative time
  cu_time = times_struct->tms_cutime;
  cs_time = times_struct->tms_cstime;


  // Free malloc'd memory
  free(token_list);
  free(times_struct);

}


// Get the files for redirection
void get_redirects(char *input, redirect_files *files) {
  char *input_copy = malloc(sizeof(char) * INPUT_LENGTH);
  strcpy(input_copy, input);
  int i, in_is_next = FALSE, out_is_next = FALSE, length = strlen(input);
  char *token;

  // Tokenize the string by the same separators as before, except that we no
  // longer break on the in or out arrows
  token = strtok(input_copy, " ()|&;\n\t");
  while (token != NULL) {
    // If we know the next token is the file name, set it to the appropriate
    // property of the files struct
    if (in_is_next == TRUE) {
      files->in = token;
      in_is_next = FALSE;
    }

    if (out_is_next == TRUE) {
      files->out = token;
      out_is_next = FALSE;
    }

    // Detect if the next file is going to be the input or output file
    if (*token == '<') {
      in_is_next = TRUE;
    }

    if (*token == '>') {
      out_is_next = TRUE;
    }

    token = strtok(NULL, " ()|&;\n\t");
  }

  // Shorten the string to leave out the redirection, making "input" just the
  // command to run
  for(i = 0; i < length; i++) {
    if (input[i] == '<' || input[i] == '>') {
      input[i - 1] = '\0';
      break;
    }
  }

}
