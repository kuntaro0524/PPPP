# -*- coding: utf-8 -*-
import cv2
import numpy as np
import sys
 
## 直線の座標を調べる  ##
def point_line(im_edge,hough):
    lines = cv2.HoughLinesP(im_edge,1,3.14/180,hough)
 
    h = lines[0][:][:].shape[0]
    x1 = np.empty(h,dtype=np.int)
    y1 = np.empty(h,dtype=np.int)
    x2 = np.empty(h,dtype=np.int)
    y2 = np.empty(h,dtype=np.int)

    for i in range(h):
        x1[i] = lines[0][i][0]
        y1[i] = lines[0][i][1]
        x2[i] = lines[0][i][2]
        y2[i] = lines[0][i][3]
 
    # 検出したすべての直線の終点座標を返す
    return x1,y1,x2,y2
 
 
## エッジ検出 ##
def find_edge(im,c1,c2,aperture_size):
 
    # 入力画像をグレースケール変換
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    # ガウンシアンフィルタで平滑化
    cv2.GaussianBlur(im_gray, (3,3), 0, im_gray)
    # 直線を膨張
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(9,9))
    dilated = cv2.dilate(im_gray, kernel)
    # Cannyアルゴリズムでエッジ検出
    im_edge = cv2.Canny(dilated, c1,c2,aperture_size)
 
    return im_edge
 
 
## 直線とコーナーを描く  ##
def drow_line_corner(im,x1,y1,x2,y2,th):
 
    # 直線を描画
    for i in range(x1.size):
        # 検出した直線の長さが25pixcel以上なら，直線を描く
        if abs(x1[i]-x2[i])>th or abs(y1[i]-y2[i])>th:
            cv2.line(im,(x1[i],y1[i]),(x2[i],y2[i]),(0,0,255), 5, 10)
 
    # カードのコーナーを円で囲んで描画
    x1_max = np.amax(x1)
    x1_min = np.amin(x1)
    x2_max = np.amax(x2)
    x2_min = np.amin(x2)
    y1_max = np.amax(y1)
    y1_min = np.amin(y1)
    y2_max = np.amax(y2)
    y2_min = np.amin(y2)
    cv2.circle(im,(x1_min,y1_min),30,[255,0,0],5)
    cv2.circle(im,(x1_max,y1_min),30,[255,0,0],5)
    cv2.circle(im,(x2_min,y2_max),30,[255,0,0],5)
    cv2.circle(im,(x2_max,y2_max),30,[255,0,0],5)
 
    return im
 
 
#######################
def main():
    im = cv2.imread(sys.argv[1])
    im_edge=find_edge(im,c1=50,c2=100,aperture_size=3)
    x1,y1,x2,y2 = point_line(im_edge,hough=25)
    im = drow_line_corner(im,x1,y1,x2,y2,th=20)
    cv2.imshow("Card Edge",im)
    cv2.waitKey(0)
    cv2.imwrite("edge_corner.jpg",im)
    cv2.destroyAllWindows()
 
#######################
if __name__ == '__main__':
    main()
