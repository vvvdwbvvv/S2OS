#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <netinet/in.h>

void vuln(char *input) {
    char buffer[64];
    strcpy(buffer, input); 
    printf("Received: %s\n", buffer);
}

int main() {
    int sockfd, clientfd;
    struct sockaddr_in server_addr, client_addr;
    char buf[1024];
    socklen_t sin_len = sizeof(client_addr);

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(1234);

    bind(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr));
    listen(sockfd, 1);
    printf("[VM] Listening on port 1234...\n");

    clientfd = accept(sockfd, (struct sockaddr *)&client_addr, &sin_len);
    read(clientfd, buf, 1024);
    vuln(buf); 

    close(clientfd);
    close(sockfd);

    printf("pwned\n");  
    return 0;
}
