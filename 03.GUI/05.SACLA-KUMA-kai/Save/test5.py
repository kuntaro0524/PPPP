def on_mouse(event, x, y, flags, params):
    if event == cv.CV_EVENT_LBUTTONDOWN:
        print 'Start Mouse Position: '+str(x)+', '+str(y)
        sbox = [x, y]
        boxes.append(sbox)
    elif event == cv.CV_EVENT_LBUTTONUP:
        print 'End Mouse Position: '+str(x)+', '+str(y)
        ebox = [x, y]
        boxes.append(ebox)

count = 0
while(1):
    count += 1
    _,img = cap.read()
    img = cv2.blur(img, (3,3))

    cv2.namedWindow('real image')
    cv.SetMouseCallback('real image', on_mouse, 0)
    cv2.imshow('real image', img)

    if count < 50:
        if cv2.waitKey(33) == 27:
            cv2.destroyAllWindows()
            break
    elif count >= 50:
        if cv2.waitKey(0) == 27:
            cv2.destroyAllWindows()
            break
        count = 0
