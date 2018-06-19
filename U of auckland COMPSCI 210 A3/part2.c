#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

/* variable declaration */
unsigned short R[8]={0,0,0,0,0,0,0,0},PC,IR;
char CC;
int programcount = 0;
int progSize, progStart, progEnd;
size_t fileSize;


short SignExtend(short val, unsigned short nBits) {
/* return the sign-extended value for the n-bit val
 * for example,
 * val=0x123, nBits=9, => return 0xff23
 * val=0x045, nBits=9, => return 0x0045
 */ 
	short temp;
	temp = val << (16 - nBits);
	temp = temp >> (16 - nBits);
	return temp;
}

	
 
/* This function disassembles one instruction by decoding the fields. */
int register_status(unsigned short mem[], unsigned short IR, short PC) {
    programcount++;
	/* declare variables to extract different fields of the IR */
	int opcode = (IR >> 12) & 0xf; /* extract IR bits 15:12 */
	int dst = (IR >> 9) & 0x7; /* IR bits 11:9 */
	short PCoffset9 = SignExtend((short)(IR & 0x1ff), 9); /* extract IR bits 8:0, then sign extend */
	int count;
    unsigned short PC2 = (unsigned short) (PC);
    int trapvect8 = IR & 0xff; /* extract IR bits 7:0 */
	switch (opcode) {
		case 2:{ /* LD */
            printf("after executing instruction\t0x%x\n",IR);
            short add = PCoffset9 + programcount + 1; /* the address for fetching the value*/
            unsigned short value_reg = *(mem+add);
            switch(dst){
                case 0: //R0
                    R[0] = value_reg;
                    break;
                case 1: //R1
                    R[1] = value_reg;
                    break;
                case 2: //R2
                    R[2] = value_reg;
                    break;
                case 3: //R3
                    R[3] = value_reg;
                    break;
                case 4: //R4
                    R[4] = value_reg;
                    break;
                case 5: //R5
                    R[5] = value_reg;
                    break;
                case 6: //R6
                    R[6] = value_reg;
                    break;
                case 7: //R7
                    R[7] = value_reg;
                    break;
            }
            if((short)(value_reg)<0){
                CC = 'N';
            }else if((short)(value_reg)==0){
                CC = 'Z';
            }else{
                CC = 'P';
            }
            for(count = 0; count<8; count++){
                if(R[count] <= 0xf ){
                    printf("R%d\t0x000%x\n",count,R[count]);
                }else if(R[count] <= 0xff){
                    printf("R%d\t0x00%x\n",count,R[count]);
                }else if(R[count] <= 0xfff){
                    printf("R%d\t0x0%x\n",count,R[count]);
                }else{
                    printf("R%d\t0x%x\n",count,R[count]);
                }
            }
            if(PC2 <= 0xf ){
                printf("PC\t0x000%x\n",PC2);
            }else if(PC2 <= 0xff){
                printf("PC\t0x00%x\n",PC2);
            }else if(PC2 <= 0xfff){
                printf("PC\t0x0%x\n",PC2);
            }else{
                printf("PC\t0x%x\n",PC2);
            }
                printf("IR\t0x%x\n",IR);
                printf("CC\t%c\n",CC);
                printf("==================\n");
            return 1;
            break;
        }
		case 0xF:{ /* TRAP */
            if(trapvect8 == 0x25)
            {
                return 0;
            }
            return 1;
            break;
        }
	}
    return 1;
}

void Disassemble(unsigned short mem[]) {
	int i;
	int status;
	printf("Initial state\n");
    printf("R0\t0x0000\n");
    printf("R1\t0x0000\n");
    printf("R2\t0x0000\n");
    printf("R3\t0x0000\n");
    printf("R4\t0x0000\n");
    printf("R5\t0x0000\n");
    printf("R6\t0x0000\n");
    printf("R7\t0x0000\n");
    if(*mem <= 0xf ){
        printf("PC\t0x000%x\n",*mem);
    }else if(*mem <= 0xff){
        printf("PC\t0x00%x\n",*mem);
    }else if(*mem <= 0xfff){
        printf("PC\t0x0%x\n",*mem);
    }else{
        printf("PC\t0x%x\n",*mem);
    }
    printf("IR\t0x0000\n");
    printf("CC\tZ\n");
    printf("==================\n");
	/* initialize used i */
    for ( i = 1; i < progSize; i++) {
		status = register_status(mem,*(mem+i),(short)(*(mem)+i));
        if (status == 0 ){
            break;
        }
    }
}
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
	Disassemble(ReadFile(argv[1]));
}