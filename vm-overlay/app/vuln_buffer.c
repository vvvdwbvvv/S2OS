#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void vulnerable_function(const char *input) {
    char buffer[256];
    strcpy(buffer, input);  // don't check copy => buffer overflow
    printf("[EXPLOIT] vulnerable_function executed with payload: %.16s...\n", input);
}

int main() {
    // make payload
    const char *path = "/mnt/host0/payload.txt";
    FILE *f = fopen(path, "w");
    if (!f) {
        perror("fopen");
        return 1;
    }

    char payload[512 + 1];
    memset(payload, 'A', 512);
    payload[512] = '\0';

    fputs(payload, f);
    fclose(f);
    printf("[EXPLOIT] Wrote payload to %s\n", path);

    // sim attack
    vulnerable_function(payload);

    return 0;
}
