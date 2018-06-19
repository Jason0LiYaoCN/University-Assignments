#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

int progSize, progStart, progEnd;
size_t fileSize;

unsigned short *ReadFile(char *filename) {
	unsigned short *mem;
	FILE *fh;
	fh = fopen(filename, "rb"); /* open as binary */
	if (fh == NULL) {
		printf("cannot open %s\n", filename);
		return 0;
	}
	/* find the file size */
	fseek(fh, 0L, SEEK_END); /* go to the end of file */
	fileSize = ftell(fh);    /* find where it is */
	fseek(fh, 0L, SEEK_SET); /* go to the beginning */
	/* now allocate a buffer of the size */
	mem = malloc(fileSize);
	if (mem == NULL) {
		printf("cannot allocate memory\n");
		return 0;
	}
	fread(mem, fileSize, 1, fh);
	fclose(fh);
	/* check if file is empty */
	if (fileSize == 0) {
		return 0;
	}
	/* check if file size is odd */
	if (fileSize % 2) {
		printf("file size is odd\n");
		return 0;
	}
	/*  big endian  */
    int i;
    progSize = fileSize / 2;
	
    for ( i = 0; i < progSize; i++) {
		mem[i] = mem[i] << 8 | ((mem[i] >> 8) & 0xff);
        if(*(mem+i) <= 0xf ){
            printf("0x000%x\n",*(mem+i));
        }else if(*(mem+i) <= 0xff){
            printf("0x00%x\n",*(mem+i));
        }else if(*(mem+i) <= 0xfff){
            printf("0x0%x\n",*(mem+i));
        }else{
            printf("0x%x\n",*(mem+i));
        }
    }
    return mem;
}
/*
 * main file to open and call the disassembler function.
 * it is ready to use. you don't have to make changes.
 */
int main(int argc, char **argv) {
	if (argc != 2) {
		fprintf(stderr, "usage: %s file.obj\n", argv[0]);
		exit(1);
	}
	ReadFile(argv[1]);
}