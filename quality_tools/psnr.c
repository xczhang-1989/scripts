#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>

#define ARG_NUM_SHORT 6
#define ARG_NUM_LONG (ARG_NUM_SHORT + 2)

double cal_psnr(uint8_t *yuv_src, uint8_t *yuv_cmp, int h, int w, double *ssd_sum)
{
  uint64_t ssd = 0;
  double d_ssd;
  double psnr;
  int x, y;

  for (y = 0; y < h; y++) {
    for (x = 0; x < w; x++) {
      int diff = yuv_src[x] - yuv_cmp[x];
      diff = diff > 255 ? 255 : diff;
      ssd += diff * diff;
    }
    yuv_src += w;
    yuv_cmp += w;
  }

  d_ssd = (double)ssd / (w * h);
  (*ssd_sum) += d_ssd;

  psnr = d_ssd ? 10.0 *log10((255 * 255) / d_ssd) : 999.99;
  return psnr;
}
int main(int argc, char *argv[])
{
  if ((argc != ARG_NUM_SHORT && argc != ARG_NUM_SHORT + 1)
    && (argc != ARG_NUM_LONG && argc != ARG_NUM_LONG + 1)) {
    printf("Err call!\n");
    printf("src.yuv cmp.yuv 1920 1080 1000 [opt]result.csv\n");
    //      1        2          3       4        5    6    7     8
    printf("src.yuv src_start, cmp.yuv cmp_start 1920 1080 1000 [opt]result.csv\n");
    exit(-1);
  }

  int width, height, frames;
  int src_start, cmp_start;
  char *src_name, *cmp_name;
  FILE *f_src = NULL, *f_cmp = NULL, *f_out = NULL;

  if (argc == ARG_NUM_SHORT || argc == ARG_NUM_SHORT + 1) {
    //cml parse
    src_name = argv[1];
    cmp_name = argv[2];


    fopen_s(&f_src, src_name, "rb");
    fopen_s(&f_cmp, cmp_name, "rb");

    if (argc == ARG_NUM_SHORT + 1) {
      fopen_s(&f_out, argv[6], "wb");

      if (NULL == f_out) {
        printf("Output file cannot open!\n");
        return -1;
      }
    }

    if (NULL == f_src) {
      printf("Src file cannot open!\n");
      return -1;
    }
    if (NULL == f_cmp) {
      printf("Cmp file cannot open!\n");
      return -1;
    }

    width = atoi(argv[3]);
    height = atoi(argv[4]);
    frames = atoi(argv[5]);

    src_start = 0;

    cmp_start = 0;

  } else {
    //      1        2          3       4        5    6    7     8
    printf("src.yuv src_start, cmp.yuv cmp_start 1920 1080 1000 [opt]result.csv\n");
    //cml parse
    src_name = argv[1];
    cmp_name = argv[3];

    fopen_s(&f_src, src_name, "rb");
    fopen_s(&f_cmp, cmp_name, "rb");

    if (argc == ARG_NUM_LONG + 1) {
      fopen_s(&f_out, argv[8], "wb");

      if (NULL == f_out) {
        printf("Output file cannot open!\n");
        return -1;
      }
    }

    if (NULL == f_src) {
      printf("Src file cannot open!\n");
      return -1;
    }
    if (NULL == f_cmp) {
      printf("Cmp file cannot open!\n");
      return -1;
    }

    src_start = atoi(argv[2]);

    cmp_start = atoi(argv[4]);


    width = atoi(argv[5]);
    height = atoi(argv[6]);
    frames = atoi(argv[7]);
  }

  int frame_size = width * height * 3 / 2;
  int y_size = width * height, uv_size = width * height >> 2;

  uint8_t *src_buf = (uint8_t *)malloc(sizeof(uint8_t) * frame_size);
  uint8_t *cmp_buf = (uint8_t *)malloc(sizeof(uint8_t) * frame_size);

  double psnr[3], ffmpeg_video_psnr[3], normal_avg_psnr[3] = {0};
  double ssd_sum[3];

  fseek(f_src, frame_size * src_start, SEEK_SET);
  fseek(f_cmp, frame_size * cmp_start, SEEK_SET);

  if (f_out != NULL) {
    fprintf(f_out, "frame, Y PSNR, U PSNR, V PSNR\n");
    for (int i = 0; i < frames; i++) {
      fread(src_buf, 1, frame_size, f_src);
      fread(cmp_buf, 1, frame_size, f_cmp);

      psnr[0] = cal_psnr(src_buf, cmp_buf, height, width, ssd_sum);
      psnr[1] = cal_psnr(src_buf + y_size, cmp_buf + y_size, height >> 1, width >> 1, ssd_sum + 1);
      psnr[2] = cal_psnr(src_buf + y_size + uv_size, cmp_buf + y_size + uv_size, height >> 1, width >> 1, ssd_sum + 2);

      normal_avg_psnr[0] += psnr[0];
      normal_avg_psnr[1] += psnr[1];
      normal_avg_psnr[2] += psnr[2];

      fprintf(f_out, "%d, %.4f, %.4f, %.4f\n", i, psnr[0], psnr[1], psnr[2]);
    }

    normal_avg_psnr[0] /= frames;
    normal_avg_psnr[1] /= frames;
    normal_avg_psnr[2] /= frames;

    //summary
    for (int ctx = 0; ctx < 3; ctx++) {
      ffmpeg_video_psnr[ctx] = (ssd_sum[ctx] ? 10.0 * log10((255 * 255) * frames / ssd_sum[ctx]) : 999.99);
    }

    fprintf(f_out, "FFMPEG AVG, %.4f, %.4f, %.4f\n", ffmpeg_video_psnr[0], ffmpeg_video_psnr[1], ffmpeg_video_psnr[2]);
    fprintf(f_out, "NORMAL AVG, %.4f, %.4f, %.4f\n", normal_avg_psnr[0], normal_avg_psnr[1], normal_avg_psnr[2]);

    fprintf(stdout, "============================\n");
    fprintf(stdout, "==========summary===========\n");
    fprintf(stdout, "FFMPEG AVG, %.4f, %.4f, %.4f\n", ffmpeg_video_psnr[0], ffmpeg_video_psnr[1], ffmpeg_video_psnr[2]);
    fprintf(stdout, "NORMAL AVG, %.4f, %.4f, %.4f\n", normal_avg_psnr[0], normal_avg_psnr[1], normal_avg_psnr[2]);

  } else {
    fprintf(stdout, "frame, Y PSNR, U PSNR, V PSNR\n");
    for (int i = 0; i < frames; i++) {
      fread(src_buf, 1, frame_size, f_src);
      fread(cmp_buf, 1, frame_size, f_cmp);

      psnr[0] = cal_psnr(src_buf, cmp_buf, height, width, ssd_sum);
      psnr[1] = cal_psnr(src_buf + y_size, cmp_buf + y_size, height >> 1, width >> 1, ssd_sum + 1);
      psnr[2] = cal_psnr(src_buf + y_size + uv_size, cmp_buf + y_size + uv_size, height >> 1, width >> 1, ssd_sum + 2);

      normal_avg_psnr[0] += psnr[0];
      normal_avg_psnr[1] += psnr[1];
      normal_avg_psnr[2] += psnr[2];

      fprintf(stdout, "%d, %.4f, %.4f, %.4f\n", i, psnr[0], psnr[1], psnr[2]);
    }

    normal_avg_psnr[0] /= frames;
    normal_avg_psnr[1] /= frames;
    normal_avg_psnr[2] /= frames;

    //summary
    for (int ctx = 0; ctx < 3; ctx++) {
      ffmpeg_video_psnr[ctx] = (ssd_sum[ctx] ? 10.0 * log10((255 * 255) * frames / ssd_sum[ctx]) : 999.99);
    }

    fprintf(stdout, "============================\n");
    fprintf(stdout, "==========summary===========\n");
    fprintf(stdout, "FFMPEG AVG, %.4f, %.4f, %.4f\n", ffmpeg_video_psnr[0], ffmpeg_video_psnr[1], ffmpeg_video_psnr[2]);
    fprintf(stdout, "NORMAL AVG, %.4f, %.4f, %.4f\n", normal_avg_psnr[0], normal_avg_psnr[1], normal_avg_psnr[2]);
  }



  free(src_buf);
  free(cmp_buf);
  fclose(f_src);
  fclose(f_cmp);
  fclose(f_out);

  return 0;
}


