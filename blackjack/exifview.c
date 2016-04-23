/*
 * Exifview
 * Author: Alex LaFroscia
 * Date: Sep 20, 2014
 */

#include<stdio.h>
#include<stdlib.h>
#include<string.h>

struct exif {
  short int start;
  short int app1_marker;
  short int app1_length;
  char      exif_string[4];
  short int exif_term;
  char      endianness[2];
  short int version;
  int       tiff_offset;
};

struct tiff {
  short int id;
  short int type;
  int num_items;
  int value;
};

struct image {
  long int width;
  long int height;
  short iso_speed;
  unsigned int exposure[2];
  unsigned int f_stop[2];
  unsigned int focal_length[2];
  char date_taken[256];
  struct exif *exif;
  char manufacturer[256];
  char model[256];
};


int main(int argc, char const *argv[]) {
  FILE *filein;
  struct exif exif_header;
  struct image *image,image_obj;
  image = &image_obj;
  unsigned short tiff_count;
  long int exif_sub_block_address;

  // If no argument is provided, print an error message and return
  if (argv[1] == NULL) {
    printf("Argment missing: filename\n");
    return 1;
  }

  // Open the file
  filein = fopen(argv[1], "rb");

  // Read in the exif header from the file
  fread(&exif_header, sizeof(struct exif), 1, filein);
  image->exif = &exif_header;

  if (strcmp(image->exif->endianness, "MM") == 0) {
    printf("Wrong endianness, exitting...\n");
    return 1;
  }

  if (strcmp(image->exif->exif_string, "Exif") != 0) {
    printf("Not a valid image file\n");
    return 1;
  }

  // Read in the number of tiff tags in the file
  fread(&tiff_count, sizeof(unsigned short), 1, filein);

  // Read in the tiff tags
  struct tiff tiff_array[tiff_count];
  fread(tiff_array, sizeof(struct tiff), tiff_count, filein);

  // Iterate over the tiff tags, pulling out the useful data
  int i;
  for(i = 0; i < tiff_count; i++) {
    struct tiff *tiff = &tiff_array[i];

    switch (tiff->id)
    {
      case 0x010f:
      case 0x0110: {
        char ascii_string[tiff->num_items];
        fseek(filein, 12 + tiff->value, SEEK_SET);
        fread(ascii_string, sizeof(char), tiff->num_items, filein);
        if (tiff->id == 0x010f) {
          strcpy(image->manufacturer, ascii_string);
        } else {
          strcpy(image->model, ascii_string);
        }
        break;
      }

      case 0xffff8769: {
        exif_sub_block_address = tiff->value;
        break;
      }
    }
  }

  // If there is an exif sub block, read the tags from there, too
  if (&exif_sub_block_address != NULL) {
    short int sub_tiff_count;
    fseek(filein, 12 + exif_sub_block_address, SEEK_SET);
    fread(&sub_tiff_count, sizeof(unsigned short), 1, filein);
    struct tiff sub_tiff_array[sub_tiff_count];
    fread(sub_tiff_array, sizeof(struct tiff), sub_tiff_count, filein);

    int i;
    for(i = 0; i < sub_tiff_count; i++) {
      struct tiff *tiff = &sub_tiff_array[i];

      switch (tiff->type) {
        case 2: {
          if (tiff->id == 0xffff9003) {
            char ascii_string[tiff->num_items];
            fseek(filein, 12 + tiff->value, SEEK_SET);
            fread(ascii_string, sizeof(char), tiff->num_items, filein);
            strcpy(image->date_taken, ascii_string);
          }
        }

        case 3: {
          if (tiff->id == 0xffff8827) {
            image->iso_speed = tiff->value;
          }
        }

        case 4: {
          if (tiff->id == 0xffffA002) {
            image->width = tiff->value;
          } else if (tiff->id == 0xffffA003) {
            image->height = tiff->value;
          }
        }

        case 5: {
          unsigned int fraction_array[2];
          fseek(filein, 12 + tiff->value, SEEK_SET);
          fread(fraction_array, sizeof(int), 2, filein);

          if (tiff->id == 0xffff829a) {
            image->exposure[0] = fraction_array[0];
            image->exposure[1] = fraction_array[1];
          } else if (tiff->id == 0xffff829d) {
            image->f_stop[0] = fraction_array[0];
            image->f_stop[1] = fraction_array[1];
          } else if (tiff->id == 0xffff920A) {
            image->focal_length[0] = fraction_array[0];
            image->focal_length[1] = fraction_array[1];
          }

        }
      } // End switch
    } // End for
  } // End if

  printf("Manufacturer:\t%s\n", image->manufacturer);
  printf("Model:\t%s\n", image->model);
  printf("Exposure Time:\t%d/%d second\n", image->exposure[0], image->exposure[1]);
  printf("F-stop:\tf/%.1f\n", (float)image->f_stop[0] / (float)image->f_stop[1]);
  printf("ISO:\tISO %d\n", image->iso_speed);
  printf("Date Taken:\t%s\n", image->date_taken);
  printf("Focal Length: %d mm\n", image->focal_length[0] / image->focal_length[1]);
  printf("Width:\t%lu pixels\n", image->width);
  printf("Height:\t%lu pizels\n", image->height);

  // Exit
  fclose(filein);
  return 0;
}

