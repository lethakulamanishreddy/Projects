import string
import tkinter
from tkinter import *
from tkinter import filedialog
import cv2
import numpy as np
from pil import Image
import img2pdf

root = tkinter.Tk()
root.geometry('900x600')
root.resizable(width=False,
             height=False
             )
root.title('Cam Scanner')


files=[]
imagelist=[]
i=0


def destroy():
    root.destroy()
   
def mapp(h):
    h = h.reshape((4,2))
    hnew = np.zeros((4,2),dtype = np.float32)
    add = h.sum(1)
    hnew[0] = h[np.argmin(add)]
    hnew[2] = h[np.argmax(add)]
    diff = np.diff(h,axis = 1)
    hnew[1] = h[np.argmin(diff)]
    hnew[3] = h[np.argmax(diff)]
    return hnew

def get_files():
    file = filedialog.askopenfilenames(parent=root,title='Choose a file')
    file = root.tk.splitlist(file)
    print ("list of filez =",file)
    files=file

def scan():
    for image in files:
       image=cv2.imread(image) 
       image=cv2.resize(image,(1300,800))
       orig=image.copy()
       gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
       blurred=cv2.GaussianBlur(gray,(5,5),0)
       edged=cv2.Canny(blurred,30,50)
       contours,hierarchy=cv2.findContours(edged,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)  
       contours=sorted(contours,key=cv2.contourArea,reverse=True)
       for c in contours:
          p=cv2.arcLength(c,True)
          approx=cv2.approxPolyDP(c,0.02*p,True)

          if len(approx)==4:
              target=approx
              break
       approx=mapp(target)
       pts=np.float32([[0,0],[800,0],[800,800],[0,800]])
       op=cv2.getPerspectiveTransform(approx,pts)
       scanned=cv2.warpPerspective(orig,op,(800,800))
       imagelist.append(scanned)
    print(imagelist)
def pdf():
    for i in imagelist:
       cv2.imshow('i',i)
##    with open("manish.pdf","wb") as f:
##       f.write(img2pdf.convert(imagelist))


b1=Button(root,
          padx=5,
          pady=5,
          width=12,
          bg='gray64',
          fg='black',
          relief=GROOVE,
          command=get_files,
          text='Select',
          font=('helvetica 15 bold'),
          activebackground='light green'
          )

b1.place(x=20,y=450)

b1=Button(root,
          padx=5,
          pady=5,
          width=12,
          bg='gray64',
          fg='black',
          relief=GROOVE,
          command=scan,
          text='Scan',
          font=('helvetica 15 bold'),
          activebackground='light green'
          )

b1.place(x=200,y=450)

b3=Button(root,
          padx=5,
          pady=5,
          width=12,
          bg='blue',
          fg='black',
          relief=GROOVE,
          text='PDF',
          command=pdf,
          font=('helvetica 15 bold'),
          activebackground='red'
          )
b3.place(x=380,y=450)

b3=Button(root,
          padx=5,
          pady=5,
          width=12,
          bg='red2',
          fg='black',
          relief=GROOVE,
          text='EXIT',
          command=destroy,
          font=('helvetica 15 bold'),
          activebackground='red'
          )
b3.place(x=540,y=450)

root.mainloop()
