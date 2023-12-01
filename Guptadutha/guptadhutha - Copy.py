'''
                           

                          Steganography is the art and  
                science of writing hidden messages in such a way 
            that no one, apart from the sender andnintended recipient

Developed by : Team SAHARA
code contributed by: MANISH REDDY LETHAKULA

'''

from stegano import  lsb
from tkinter import filedialog
from tkinter import simpledialog
import tkinter
from tkinter import *

root = tkinter.Tk()
root.geometry('799x500')
root.resizable(width=False,
               height=False
              )

root.title('Guptaduta')

filename = PhotoImage(file="bg1.png")
background_label = Label(root,
                         image=filename
                         )
background_label.place(x=0,y=0)


statusbar=Label(root,
                width=79,
                text="A project by Uday, jgsjh, jfkf",
                font=("arial",13,"bold"),
                bg="black",
                fg="white",
                relief=SUNKEN
                )

statusbar.place(x=2,y=476)

def destroy():
    root.destroy()


def encode():
   text = simpledialog.askstring(title="Secret message",
                                  prompt="What's the message?")

   file = filedialog.askopenfilenames(parent=root,
                                      title='Choose a image')
   file=file[0]
   secret = lsb.hide(file, text)
   secret.save("./secret.png")
   msg="Messeage is encoded and saved as 'secret.png'"
   messagebox.showinfo("info",msg)


def decode():
   file = filedialog.askopenfilenames(parent=root,title='Choose a image')
   file=file[0]
   msg=lsb.reveal(file)
   messagebox.showinfo("Secret message is",msg)  


b1=Button(root,
          padx=5,
          pady=5,
          width=12,
          bg='DodgerBlue1',
          fg='white',
          relief=GROOVE,
          command=encode,
          text='Encode',
          font=('helvetica 15 bold'),
          activebackground='light green'
          )

b1.place(x=100,y=300)

b2=Button(root,
          padx=5,
          pady=5,
          width=12,
          bg='green3',
          fg='white',
          relief=GROOVE,
          text='Decode',
          command=decode,
          font=('helvetica 15 bold'),
          activebackground='red'
          )
b2.place(x=315,y=300)

b3=Button(root,
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
b3.place(x=525,y=300)
root.mainloop()
