#from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
import string
import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog




root = tkinter.Tk()
root.geometry('850x600')
root.resizable(width=False,
             height=False
             )
root.title('VISHWAKARMA')
root.config(bg="azure3")
title=Label(root,
            text='VISHWAKARMA',
            font=("times",29,"bold"),
            bg="azure3",
            fg="black",
            #relief=SUNKEN
            )
title.place(x=250,y=2)


statusbar=Label(root,
                width=90,
                text="A project by Team SAHARA   ",
                font=("arial",13,"bold"),
                bg="black",
                fg="white",
                relief=SUNKEN
                )

statusbar.place(x=0,y=575)


files=['']
model='model/colorization_release_v2.caffemodel'
prototxt='model/colorization_deploy_v2.prototxt'
points='model/pts_in_hull.npy'
net = cv2.dnn.readNetFromCaffe(prototxt,model)
pts = np.load(points)
class8 = net.getLayerId("class8_ab")
conv8 = net.getLayerId("conv8_313_rh")
pts = pts.transpose().reshape(2, 313, 1, 1)
net.getLayer(class8).blobs = [pts.astype("float32")]
net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]

def cam():
   print(" Starting webcam video stream...")
   #vs = VideoStream(src=0).start()
   vs=cv2.VideoCapture(0)
   time.sleep(1.0)
   while True:
      _,frame = vs.read()
      frame = imutils.resize(frame, width=500)
      scaled = frame.astype("float32") / 255.0
      lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)
      resized = cv2.resize(lab, (224, 224))
      L = cv2.split(resized)[0]
      L-=50
      net.setInput(cv2.dnn.blobFromImage(L))
      ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
      ab = cv2.resize(ab, (frame.shape[1], frame.shape[0]))
      L = cv2.split(lab)[0]
      colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)
      colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
      colorized = np.clip(colorized, 0, 1)
      colorized = (255 * colorized).astype("uint8")
      cv2.imshow("Original", frame)
      cv2.imshow("Grayscale", cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
      cv2.imshow("Colorized", colorized)
      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
         break
   vs.release()
   cv2.destroyAllWindows()

def video():
   file = filedialog.askopenfilenames(parent=root,title='Choose a file')
   file = root.tk.splitlist(file)
   print(file[0])
   files[0]=file[0]
   path=str(files[0])
   vs=cv2.VideoCapture(path)
   #cap = cv2.VideoCapture(0)
   width = int(vs.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
   height = int(vs.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
   size = (width, height)
   fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
   out = cv2.VideoWriter('new1.avi', fourcc, 24.0, size)   
   #time.sleep(1.0)
   while True:
      ret,frame = vs.read()
      if ret==True:
      #frame = imutils.resize(frame, width=500)
         scaled = frame.astype("float32") / 255.0
         lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)
         resized = cv2.resize(lab, (224, 224))
         L = cv2.split(resized)[0]
         L-=50
         net.setInput(cv2.dnn.blobFromImage(L))
         ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
         ab = cv2.resize(ab, (frame.shape[1], frame.shape[0]))
         L = cv2.split(lab)[0]
         colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)
         colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
         colorized = np.clip(colorized, 0, 1)
         colorized = (255 * colorized).astype("uint8")
         out.write(colorized) 
         cv2.imshow("Original", frame)
         cv2.imshow("Grayscale", cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
         cv2.imshow("Colorized", colorized)
         
         key = cv2.waitKey(1) & 0xFF
         if key == ord("q"):
            break
      else :break
   vs.release()
   out.release
   cv2.destroyAllWindows()


def colorimage():
   file = filedialog.askopenfilenames(parent=root,title='Choose a file')
   file = root.tk.splitlist(file)
   print(file[0])
   files[0]=file[0]
   path=str(files[0])
   image = cv2.imread(path)
   image=imutils.resize(image,width=500)
   scaled = image.astype("float32") / 255.0
   lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)
   resized = cv2.resize(lab, (224, 224))
   L = cv2.split(resized)[0]
   L -= 50
   net.setInput(cv2.dnn.blobFromImage(L))
   ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
   ab = cv2.resize(ab, (image.shape[1], image.shape[0]))
   L = cv2.split(lab)[0]
   colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)
   colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
   colorized = np.clip(colorized, 0, 1)
   colorized = (255 * colorized).astype("uint8")
   cv2.imshow("Original", image)
   cv2.imshow("Grayscale", cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
   cv2.imshow("Colorized", colorized)
   #cv2.imshow("lab",lab) 
   cv2.waitKey(0)

def destroy():
    root.destroy()


b1=Button(root,
          padx=5,
          pady=5,
          width=12,
          bg='DodgerBlue1',
          fg='white',
          relief=GROOVE,
          command=colorimage,
          text='SELECT IMG',
          font=('helvetica 15 bold'),
          activebackground='light green'
          )

b1.place(x=50,y=300)

b2=Button(root,
          padx=5,
          pady=5,
          width=12,
          bg='gray64',
          fg='white',
          relief=GROOVE,
          command=cam,
          text='Webcam',
          font=('helvetica 15 bold'),
          activebackground='light green'
          )

b2.place(x=250,y=300)

b3=Button(root,
          padx=5,
          pady=5,
          width=12,
          bg='gray64',
          fg='white',
          relief=GROOVE,
          command=video,
          text='Video Input',
          font=('helvetica 15 bold'),
          activebackground='light green'
          )

b3.place(x=450,y=300)


b4=Button(root,
          padx=5,
          pady=5,
          width=12,
          bg='orange red',
          fg='white',
          relief=GROOVE,
          text='EXIT',
          command=destroy,
          font=('helvetica 15 bold'),
          activebackground='red'
          )
b4.place(x=650,y=300)
root.mainloop()

 
