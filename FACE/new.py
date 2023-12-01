import cv2
cap = cv2.VideoCapture(0)
while True:
    _, img = cap.read()
    img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cv2.imshow('Color',img)
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break
cap.release()

cv2.destroyAllWindows()
