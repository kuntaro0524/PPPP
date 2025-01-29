#include <cv.h>
#include <highgui.h>

/* プロトタイプ宣言 */
void cvShiftDFT (CvArr * src_arr, CvArr * dst_arr);

int
main (int argc, char **argv)
{
  IplImage *src_img;
  IplImage *realInput;
  IplImage *imaginaryInput;
  IplImage *complexInput;
  IplImage *image_Re;
  IplImage *image_Im;
  int dft_M, dft_N;
  CvMat *dft_A, tmp;
  double m, M;

  src_img = cvLoadImage (argv[1], CV_LOAD_IMAGE_GRAYSCALE);
  if (!src_img)
    return -1;

  realInput = cvCreateImage (cvGetSize (src_img), IPL_DEPTH_64F, 1);
  imaginaryInput = cvCreateImage (cvGetSize (src_img), IPL_DEPTH_64F, 1);
  complexInput = cvCreateImage (cvGetSize (src_img), IPL_DEPTH_64F, 2);

  // (1)入力画像を実数配列にコピーし，虚数配列とマージして複素数平面を構成
  cvScale (src_img, realInput, 1.0, 0.0);
  cvZero (imaginaryInput);
  cvMerge (realInput, imaginaryInput, NULL, NULL, complexInput);

  // (2)DFT用の最適サイズを計算し，そのサイズで行列を確保する
  dft_M = cvGetOptimalDFTSize (src_img->height - 1);
  dft_N = cvGetOptimalDFTSize (src_img->width - 1);
  dft_A = cvCreateMat (dft_M, dft_N, CV_64FC2);
  image_Re = cvCreateImage (cvSize (dft_N, dft_M), IPL_DEPTH_64F, 1);
  image_Im = cvCreateImage (cvSize (dft_N, dft_M), IPL_DEPTH_64F, 1);

  // (3)複素数平面をdft_Aにコピーし，残りの行列右側部分を0で埋める
  cvGetSubRect (dft_A, &tmp, cvRect (0, 0, src_img->width, src_img->height));
  cvCopy (complexInput, &tmp, NULL);
  if (dft_A->cols > src_img->width) {
    cvGetSubRect (dft_A, &tmp, cvRect (src_img->width, 0, dft_A->cols - src_img->width, src_img->height));
    cvZero (&tmp);
  }

  // (4)離散フーリエ変換を行い，その結果を実数部分と虚数部分に分解
  cvDFT (dft_A, dft_A, CV_DXT_FORWARD, complexInput->height);
  cvSplit (dft_A, image_Re, image_Im, 0, 0);

  // (5)スペクトルの振幅を計算 Mag = sqrt(Re^2 + Im^2)
  cvPow (image_Re, image_Re, 2.0);
  cvPow (image_Im, image_Im, 2.0);
  cvAdd (image_Re, image_Im, image_Re, NULL);
  cvPow (image_Re, image_Re, 0.5);

  // (6)振幅の対数をとる log(1 + Mag)
  cvAddS (image_Re, cvScalarAll (1.0), image_Re, NULL);
  cvLog (image_Re, image_Re);

  // (7)原点（直流成分）が画像の中心にくるように，画像の象限を入れ替える
  cvShiftDFT (image_Re, image_Re);

  // (8)振幅画像のピクセル値が0.0-1.0に分布するようにスケーリング
  cvMinMaxLoc (image_Re, &m, &M, NULL, NULL, NULL);
  cvScale (image_Re, image_Re, 1.0 / (M - m), 1.0 * (-m) / (M - m));

  cvNamedWindow ("Image", CV_WINDOW_AUTOSIZE);
  cvShowImage ("Image", src_img);
  cvNamedWindow ("Magnitude", CV_WINDOW_AUTOSIZE);
  cvShowImage ("Magnitude", image_Re);
  cvWaitKey (0);

  cvDestroyWindow ("Image");
  cvDestroyWindow ("Magnitude");
  cvReleaseImage (&src_img);
  cvReleaseImage (&realInput);
  cvReleaseImage (&imaginaryInput);
  cvReleaseImage (&complexInput);
  cvReleaseImage (&image_Re);
  cvReleaseImage (&image_Im);
  cvReleaseMat (&dft_A);

  return 0;
}

/* 原点（直流成分）が画像の中心にくるように，画像の象限を入れ替える関数．
   src_arr, dst_arr は同じサイズ，タイプの配列 */
void
cvShiftDFT (CvArr * src_arr, CvArr * dst_arr)
{
  CvMat *tmp = 0;
  CvMat q1stub, q2stub;
  CvMat q3stub, q4stub;
  CvMat d1stub, d2stub;
  CvMat d3stub, d4stub;
  CvMat *q1, *q2, *q3, *q4;
  CvMat *d1, *d2, *d3, *d4;

  CvSize size = cvGetSize (src_arr);
  CvSize dst_size = cvGetSize (dst_arr);
  int cx, cy;

  if (dst_size.width != size.width || dst_size.height != size.height) {
    cvError (CV_StsUnmatchedSizes, "cvShiftDFT", "Source and Destination arrays must have equal sizes", __FILE__,
             __LINE__);
  }
  // (9)インプレースモード用のテンポラリバッファ
  if (src_arr == dst_arr) {
    tmp = cvCreateMat (size.height / 2, size.width / 2, cvGetElemType (src_arr));
  }
  cx = size.width / 2;          /* 画像中心 */
  cy = size.height / 2;

  // (10)1〜4象限を表す配列と，そのコピー先
  q1 = cvGetSubRect (src_arr, &q1stub, cvRect (0, 0, cx, cy));
  q2 = cvGetSubRect (src_arr, &q2stub, cvRect (cx, 0, cx, cy));
  q3 = cvGetSubRect (src_arr, &q3stub, cvRect (cx, cy, cx, cy));
  q4 = cvGetSubRect (src_arr, &q4stub, cvRect (0, cy, cx, cy));
  d1 = cvGetSubRect (src_arr, &d1stub, cvRect (0, 0, cx, cy));
  d2 = cvGetSubRect (src_arr, &d2stub, cvRect (cx, 0, cx, cy));
  d3 = cvGetSubRect (src_arr, &d3stub, cvRect (cx, cy, cx, cy));
  d4 = cvGetSubRect (src_arr, &d4stub, cvRect (0, cy, cx, cy));

  // (11)実際の象限の入れ替え
  if (src_arr != dst_arr) {
    if (!CV_ARE_TYPES_EQ (q1, d1)) {
      cvError (CV_StsUnmatchedFormats, "cvShiftDFT", "Source and Destination arrays must have the same format",
               __FILE__, __LINE__);
    }
    cvCopy (q3, d1, 0);
    cvCopy (q4, d2, 0);
    cvCopy (q1, d3, 0);
    cvCopy (q2, d4, 0);
  }
  else {                        /* インプレースモード */
    cvCopy (q3, tmp, 0);
    cvCopy (q1, q3, 0);
    cvCopy (tmp, q1, 0);
    cvCopy (q4, tmp, 0);
    cvCopy (q2, q4, 0);
    cvCopy (tmp, q2, 0);
  }
}

