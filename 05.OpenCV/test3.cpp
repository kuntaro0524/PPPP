#include <cv.h>
#include <highgui.h>

int
main (int argc, char **argv)
{
  IplImage *src_img, *dst_img1, *dst_img2, *dst_img3;
  IplImage *tmp_img;

  // (1)画像の読み込み
  if (argc != 2 || (src_img = cvLoadImage (argv[1], CV_LOAD_IMAGE_GRAYSCALE)) == 0)
    return -1;

  dst_img1 = cvCreateImage (cvGetSize (src_img), IPL_DEPTH_8U, 1);

  // (5)画像の表示
  cvSaveImage ("test.jpg",src_img);
  cvReleaseImage (&src_img);
  return 0;
}

