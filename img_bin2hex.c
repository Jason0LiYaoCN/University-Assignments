#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

const char out_file_name[] = "temp";

int main(int argc, char *argv[])
{
    int ret, i, wb;
    char buffer[256];
    char fstr[16];
	uint8_t value_w8 = 0;
    uint16_t value_w16 = 0;
    uint32_t value_w32 = 0;
    int length;
    int spreat_size;
    int spreat_cnt=0;
    int out_file_cnt=0;
    int w_size;
    FILE *fin;
    FILE *fout1;
    FILE *fout2;
    FILE *fout3;

    if(argc < 4) {
        printf("Usage: %s <input-filename> <word-size(2/4)> <separate-size> <out-filename>\n", argv[0]);
        return -1;
    }

    value_w16 = 0;
    value_w32 = 0;

    fin = fopen (argv[1], "r");
    w_size = atoi(argv[2]);
    if (w_size != 2 && w_size != 1) {
        w_size = 4;
    }
    spreat_size = atoi(argv[3]);

    printf("Convert %s to Hex (Word Size %u, Saperate Size %uK)\n", argv[1], w_size, spreat_size);


    /* Input file and two output files are now open */
    /* Read input and put into output */
    i = 0;
//    while((ret = read(rdHdl, &buffer[0], sizeof(buffer))) > 0) {
    while(!feof(fin)) {
		if (w_size == 1) {
            length = fread(&value_w8 , 1 , 1 , fin );
        } else if (w_size == 2) {
            length = fread(&value_w16 , 1 , 2 , fin );
        } else {
            length = fread(&value_w32 , 1 , 4 , fin );
        }

        if (spreat_cnt == 0) {
            memset(buffer, 0, sizeof(buffer));
//            strncpy(buffer, argv[1], sizeof(buffer));
            if (argc >=5) {
                strncpy(buffer, argv[4], sizeof(buffer));
            } else {
                strncpy(buffer, out_file_name, sizeof(buffer));
            }
            strcat(buffer, "_");
//            itoa(out_file_cnt, fstr, 10);
            fstr[0] = 0x30 + out_file_cnt;
            fstr[1] = 0;
            strcat(buffer, fstr);
            strcat(buffer, ".hex");
            fout1 = fopen (buffer, "w");
            printf ("Out File: %s\r\n", buffer);
        }
//        printf ("value = 0x%08x\r\n", value_w);

        spreat_cnt += w_size;
		if (w_size == 1) {
            fprintf (fout1, "%02x", value_w8);
        } else if (w_size == 2) {
            fprintf (fout1, "%04x", value_w16);
        } else {
            fprintf (fout1, "%08x", value_w32);
        }

        if (spreat_cnt == (spreat_size * 1024)) {
            fclose(fout1);
            spreat_cnt = 0;
            out_file_cnt++;
        } else {
            fprintf (fout1, "\r\n");
        }
    }

    fclose(fin);
    if (spreat_cnt > 0) {
        fclose(fout1);
    }
    // print success
    return 0;
}
