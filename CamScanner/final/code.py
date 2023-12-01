'''


                                    The SCANNER


                    The SCANNER is a application which is similar to
                  any other doument scanners available which will take 
                images as input and extract only the required information 
             from the images using perspective transorm for getting Bird View
           and then converts all these images into a PDF file on a single click


Developed by : Team SAHARA
code contributed by: MANISH REDDY LETHAKULA

'''

import string
import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
import cv2
import numpy as np
import img2pdf
import os
import shutil

root = tkinter.Tk()
root.geometry('1200x700')
root.resizable(width=False,
             height=False
             )
root.title('The Scanner')
filename = PhotoImage(file="bg1.png")
background_label = Label(root,
                         image=filename
                         )
background_label.place(x=0,y=0)
label = Label(root,
              text="THE SCANNER",
              bg='lemon chiffon',
              font=('helvetica 30 bold'))
label.pack(side=TOP)

statusbar=Label(root,
                width=120,
                text="A project by Team SAHARA",
                font=("arial",13,"bold"),
                bg="black",
                fg="white",
                relief=SUNKEN
                )

statusbar.place(x=0,y=675)


files=[]
imagelist=[]

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
    print(len(file),'files selected')
    files.append(file)

def scan():
    i=1
    file=files[0]
    print(file)
    for image in file:
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
       pts=np.float32([[0,0],[1300,0],[1300,800],[0,800]])
       op=cv2.getPerspectiveTransform(approx,pts)
       scanned=cv2.warpPerspective(orig,op,(800,800))
       if not os.path.exists('temp'):
          os.makedirs('temp')
          print('Directory created')
       name='temp/'+str(i)+'.jpg'
       print('image '+ str(i)+' processed')
       cv2.imwrite(name,scanned)
       i+=1
def pdf():
    dirname='temp/'
    fname=simpledialog.askstring(title="filename",prompt="Enter the file name...")
    
    n=fname+'.pdf'
    with open(n,"wb") as f:
       imgs = []
       for fname in os.listdir(dirname):
          if not fname.endswith(".jpg"):
              continue
          path = os.path.join(dirname, fname)
          if os.path.isdir(path):
              continue
          imgs.append(path)
       f.write(img2pdf.convert(imgs))
    shutil.rmtree('temp')
    print('pdf created')

b1=Button(root,
          padx=5,
          pady=5,
          width=12,
          bg='DodgerBlue1',
          fg='white',
          relief=GROOVE,
          command=get_files,
          text='(1) SELECT',
          font=('helvetica 15 bold'),
          activebackground='light green'
          )

b1.place(x=125,y=550)

b2=Button(root,
          padx=5,
          pady=5,
          width=12,
          bg='gray64',
          fg='white',
          relief=GROOVE,
          command=scan,
          text='(2) SCAN',
          font=('helvetica 15 bold'),
          activebackground='light green'
          )

b2.place(x=375,y=550)

b3=Button(root,
          padx=5,
          pady=5,
          width=12,
          bg='green3',
          fg='white',
          relief=GROOVE,
          text='(3) PDF',
          command=pdf,
          font=('helvetica 15 bold'),
          activebackground='red'
          )
b3.place(x=625,y=550)

b4=Button(root,
          padx=5,
          pady=5,
          width=12,
          bg='orange red',
          fg='white',
          relief=GROOVE,
          text='(4)EXIT',
          command=destroy,
          font=('helvetica 15 bold'),
          activebackground='red'
          )
b4.place(x=875,y=550)

root.mainloop()
