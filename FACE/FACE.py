import cv2

eye = cv2.CascadeClassifier("haarcascade_fullbody.xml")
face=cv2.CascadeClassifier("haarcascade_frontalface_default.xml") 
cap = cv2.VideoCapture(0)
while True:
    _, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eyes = eye.detectMultiScale(gray, 1.1, 4)
    faces = face.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in eyes:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.imshow('facedetection', img)
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break
cap.release()

