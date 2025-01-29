/* 
 *   client.c --- 
 *       ./client hostname portnumber
 *
 */
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/uio.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    static char msg0[] = "get/bl_32in_st2_counter_1/query\n";
    static char msg1[] = "get/bl_32in_st2_counter_1/query\n";
    static char msg2[] = "get/bl_32in_st2_counter_1/query\n";
    static char msg3[] = "get/bl_32in_st2_counter_1/query\n";
    static char msg4[] = "get/bl_32in_st2_counter_1/query\n";

    int sock;                  
    struct hostent *hp;        
    struct sockaddr_in server; 
    char buf[2000];

    sock = socket(PF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
	perror("opening stream socket");
	exit(1);
    }

    hp = gethostbyname("172.24.242.41");
    if (hp == 0) {
	fprintf(stderr, "%s: unknown host\n", argv[1]);
	exit(2);
    }

    server.sin_family = AF_INET; 

    bcopy((char *)hp->h_addr, (char *)&server.sin_addr, 
	  hp->h_length);  

    server.sin_port = htons(10101);  

    if (connect(sock, (struct sockaddr *)&server, 
		sizeof server) < 0) {
	perror("connecting stream socket");
	exit(1);
    }

    if (write(sock, msg0, sizeof(msg0) - 1) < 0) {
	perror("writing on stream socket");
    }
 
    read(sock,buf,2000);
    printf("%s\n",buf);

    close(sock);
    exit(0);
}

