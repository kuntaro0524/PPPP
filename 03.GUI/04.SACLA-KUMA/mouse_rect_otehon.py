import cv2
import copy
import sys

WIDTH = 640
HEIGHT = 480
SELECT_COLOUR = (255, 0, 0)  # blue
SAVE_COLOUR = (0, 255, 0)    # green
_drawing = False
_x = _y = 0
_original = _cropped = None
default_ouput = "cropped.jpg"


def init():
    original = cv2.imread(sys.argv[1])
    cv2.namedWindow('Original image')
    cv2.imshow('Original image', original)
    cropped = original[0:HEIGHT, 0:WIDTH]  # [y, x] instead of the usual [x, y]
    cv2.namedWindow('Cropped')
    cv2.imshow("Cropped", cropped)
    return  original, cropped

def update(x, y, colour=SELECT_COLOUR):
    '''Displays original image with coloured rectangle indicating cropping area
       and updates the displayed cropped image'''
    global _x, _y, _original, _cropped
    _x, _y = x, y
    _cropped = _original[y:y+HEIGHT, x:x+WIDTH]

    cv2.imshow("Cropped", _cropped)
    img = copy.copy(_original)
    cv2.rectangle(img, (x, y), (x+WIDTH, y+HEIGHT), colour, 3)
    cv2.imshow('Original image', img)


def show_cropped(event, x, y, flags, param):
    '''Mouse callback function - updates position of mouse and determines
       if image display should be updated.'''
    global _drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        _drawing = True
    elif event == cv2.EVENT_LBUTTONUP:
        _drawing = False

    if _drawing:
        update(x, y)


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
