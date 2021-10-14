import cv2

cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

def nothing1():
    pass

cv2.namedWindow('Upper yellow threshhold')
cv2.createTrackbar('Upper_yellow_threshhold', 'Upper yellow threshhold', 0, 255, nothing1)

def contourAreaFinder(Frame):

    splitF = cv2.cvtColor(Frame, cv2.COLOR_BGR2YUV)

    frameY, frameU, frameV = cv2.split(splitF)

    ret, Mask = cv2.threshold(frameU, UpperThresh, 255, cv2.THRESH_BINARY_INV)

    contours, hierarchy = cv2.findContours(Mask, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        c = max(contours, key = cv2.contourArea)

    else:
        return 0

    return cv2.contourArea(c)

while True:
    ret, frame = cap.read()
    blurredFrame = cv2.medianBlur(frame, 13)
    YUV = cv2.cvtColor(blurredFrame, cv2.COLOR_BGR2YUV)
    UpperThresh = cv2.getTrackbarPos('Upper_yellow_threshhold', 'Upper yellow threshhold')
    y, u, v = cv2.split(YUV)
    ret, Mask2 = cv2.threshold(u, UpperThresh, 255, cv2.THRESH_BINARY_INV)
    left = blurredFrame[0:500, 0:200]
    mid = blurredFrame[0:500, 200:400]
    right = blurredFrame[0:500, 400:600]

    leftArea = contourAreaFinder(left)
    midArea = contourAreaFinder(mid)
    rightArea = contourAreaFinder(right)

    Maxareavars = {'Left':leftArea, 'Middle':midArea, 'Right':rightArea}
    if(leftArea + midArea + rightArea) > 0:
        print(max(Maxareavars.items(), key=lambda i: i[1]))
    else:
        print("none")

    cv2.imshow('Input', frame)
    cv2.imshow('left', left)
    cv2.imshow('mid', mid)
    cv2.imshow('right', right)
    cv2.imshow('test', Mask2)


    # Press ESC to quit

    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()
