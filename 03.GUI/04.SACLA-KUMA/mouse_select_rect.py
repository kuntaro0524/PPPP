import cv2
import copy
import sys
import numpy as np

WIDTH = 640
HEIGHT = 480
SELECT_COLOUR = (255, 0, 0)  # blue
SAVE_COLOUR = (0, 255, 0)    # green
_drawing = False
_started = False
_x = _y = 0
_locked = False
_original = _cropped = None
default_ouput = "cropped.jpg"

def init():
    original = cv2.imread(sys.argv[1])
    cv2.namedWindow('Original image')
    cv2.imshow('Original image', original)
    cropped = original[0:HEIGHT, 0:WIDTH]  # [y, x] instead of the usual [x, y]
    cv2.namedWindow('Cropped')
    cv2.imshow("Cropped", cropped)
    return original, cropped

'''Displays original image with coloured rectangle indicating cropping area
   and updates the displayed cropped image'''
def update(endx, endy, colour=SELECT_COLOUR):
    print "UPDATE"
    global _x, _y, _original, _cropped

    img = copy.copy(_original)
    cv2.rectangle(img, (_x, _y), (endx, endy), colour, 3)
    cenx=(_x+endx)/2.0
    ceny=(_y+endy)/2.0
    cv2.circle(img,(cenx,ceny),5,(0,0,255),2)

    width=np.fabs(cenx-_x)
    height=np.fabs(ceny-_y)

    location=(0,30)
    fontscale=1.0
    color=(255,190,0) #sky blue  
    fontface=cv2.FONT_HERSHEY_PLAIN
    msg="Rectanglar Width = %5d , Height = %5d"%(width,height)
    cv2.putText(img,msg,location,fontface,fontscale,color)  

    cv2.imshow('Original image', img)
    return cenx,ceny

def show_cropped(event, x, y, flags, param):
    '''Mouse callback function - updates position of mouse and determines
       if image display should be updated.'''
    global _drawing,_x,_y,_locked,_started
    endx,endy=0,0

    if event == cv2.EVENT_RBUTTONDOWN:
	print "Locked = false"
	_x,_y=0,0
        update(0,0)
	_locked=False
	_started=False

    if event == cv2.EVENT_LBUTTONDOWN:
	#print _locked,_drawing
	if _locked==False:
        	_drawing = True
		_started = True
		_x,_y=x,y
		endx,endy=x,y
	else:
		_drawing = False
		print "ONakaippai"

    if event == cv2.EVENT_LBUTTONUP:
	print "BUTTONUP"
        _drawing = False
	endx,endy=x,y
	_started=False
	_locked=True

    if event == cv2.EVENT_MOUSEMOVE:
	if _started==False or _locked==True:
		_drawing=False
	else:
		print "Korekarakakuyo",_started,_locked
        	_drawing = True
		print "MOVING",x,y
		endx,endy=x,y

    if _drawing:
        print "DRAWING",_x,_y,endx,endy
        cenx,ceny=update(endx,endy)
	print cenx,ceny

def main():
    '''Entry point'''
    global _original, _cropped
    _original, _cropped = init()

    cv2.setMouseCallback('Original image', show_cropped)

    while True:
        key = cv2.waitKey(1) & 0xFF  # 0xFF is for 64 bit computer
        if key == 27:  # escape
            break
        elif key == ord("s"):
            cv2.imwrite(args["output"], _cropped)
            update(_x, _y, colour=SAVE_COLOUR)

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
