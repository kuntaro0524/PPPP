#include <cv.h>
#include <highgui.h>

int
main (int argc, char *argv[])
{
  int i;
  IplImage *src_img = 0;
  IplImage *src_img_gray = 0;
  IplImage *tmp_img;
  CvMemStorage *storage = cvCreateMemStorage (0);
  CvSeq *contours = 0;
  CvPoint *point, *tmp;
  CvSeq *contour;
  CvTreeNodeIterator it;
  CvFileStorage *fs;

  if (argc >= 2)
    src_img = cvLoadImage (argv[1], CV_LOAD_IMAGE_COLOR);
  if (src_img == 0)
    return -1;

  src_img_gray = cvCreateImage (cvGetSize (src_img), IPL_DEPTH_8U, 1);
  cvCvtColor (src_img, src_img_gray, CV_BGR2GRAY);
  tmp_img = cvCreateImage (cvGetSize (src_img), IPL_DEPTH_8U, 1);

  // (1)画像の二値化と輪郭の検出
  cvThreshold (src_img_gray, tmp_img, 120, 255, CV_THRESH_BINARY);
  cvFindContours (tmp_img, storage, &contours, sizeof (CvContour), CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE);

  /* 輪郭シーケンスから座標を取得 */
  fs = cvOpenFileStorage ("contours.yaml", 0, CV_STORAGE_WRITE);
  // (2)ツリーノードイテレータの初期化
  cvInitTreeNodeIterator (&it, contours, 1);
  // (3)各ノード（輪郭）を走査
  while ((contour = (CvSeq *) cvNextTreeNode (&it)) != NULL) {
    cvStartWriteStruct (fs, "contour", CV_NODE_SEQ);
    // (4)輪郭を構成する頂点座標を取得
    tmp = CV_GET_SEQ_ELEM (CvPoint, contour, -1);
    for (i = 0; i < contour->total; i++) {
      point = CV_GET_SEQ_ELEM (CvPoint, contour, i);
      cvLine (src_img, *tmp, *point, CV_RGB (0, 0, 255), 2);
      cvStartWriteStruct (fs, NULL, CV_NODE_MAP | CV_NODE_FLOW);
      cvWriteInt (fs, "x", point->x);
      cvWriteInt (fs, "y", point->y);
      cvEndWriteStruct (fs);
      tmp = point;
    }
    cvEndWriteStruct (fs);
  }
  cvReleaseFileStorage (&fs);

  cvNamedWindow ("Contours", CV_WINDOW_AUTOSIZE);
  cvShowImage ("Contours", src_img);
  cvWaitKey (0);

  cvDestroyWindow ("Contours");
  cvReleaseImage (&src_img);
  cvReleaseImage (&src_img_gray);
  cvReleaseImage (&tmp_img);
  cvReleaseMemStorage (&storage);

  return 0;
}

