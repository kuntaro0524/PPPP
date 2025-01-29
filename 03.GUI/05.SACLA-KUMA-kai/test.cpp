#include <cv.h>
#include <highgui.h>

IplImage *dsp_img = 0;
CvPoint prev_pt = {-1,-1};

void on_mouse(int event, int x, int y, int flags, void* param)
{
	if(event == CV_EVENT_LBUTTONUP || !(flags & CV_EVENT_FLAG_LBUTTON)){
        prev_pt = cvPoint(-1,-1);
	}else if(event == CV_EVENT_LBUTTONDOWN){
        prev_pt = cvPoint(x,y);
	}else if(event == CV_EVENT_MOUSEMOVE && (flags & CV_EVENT_FLAG_LBUTTON)){
        CvPoint pt = cvPoint(x,y);
		if( prev_pt.x < 0 ){
            prev_pt = pt;
		}
        cvLine(dsp_img, prev_pt, pt, cvScalarAll(255), 5, 8, 0);
        prev_pt = pt;
        cvShowImage("image", dsp_img);
	}
}

int main (int argc, char **argv)
{
	IplImage *src_img = 0, *dst_img = 0;

	src_img = cvLoadImage("fruits.jpg", CV_LOAD_IMAGE_COLOR);
	if(src_img == 0){
		exit(-1);
	}
	dsp_img = cvCloneImage (src_img);

	cvNamedWindow("image", CV_WINDOW_AUTOSIZE);
	cvShowImage("image", src_img);
	cvSetMouseCallback("image", on_mouse, 0);
	cvWaitKey (0);
        cvReleaseImage(&src_img);
	cvReleaseImage(&dsp_img);
}
