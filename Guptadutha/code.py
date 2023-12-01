'''
                                 CIPHERE

                          Steganography is the art and  
                science of writing hidden messages in such a way 
            that no one, apart from the sender andnintended recipient

by: N. SURYA ABHIRAM-177Y1A04G6
    A. MANISH-177Y1A04D6

'''

from stegano import  lsb
from tkinter import filedialog
from tkinter import simpledialog
import tkinter
from tkinter import *

global pw

root = tkinter.Tk()
root.geometry('637x357')
##root.resizable(width=False,
##               height=False
##              )

root.title('                                         \
                                            CIPHERE')

##filename = PhotoImage(file="1.png")
##background_label = Label(root,
##                         image=filename
##                         )
##background_label.place(x=0,y=0)


def encode():
   global pw
   pw = simpledialog.askstring(title="Set password",
                                  prompt="Create a password for authenticity")

  
   text = simpledialog.askstring(title="Secret message",
                                  prompt="What's the message?")
   textfinal=pw+text

   file = filedialog.askopenfilenames(parent=root,
                                      title='Choose a image')
   file=file[0]
   secret = lsb.hide(file, textfinal)
   secret.save("secret.png")
   msg="Messeage is encoded and saved as 'secret.png'"
   messagebox.showinfo("info",msg)


def decode():
   global pw
   file = filedialog.askopenfilenames(parent=root,title='Choose a image')
   file=file[0]
   gp = simpledialog.askstring(title="Enter password",
                                  prompt="Enter your password revealing message")
   msg=lsb.reveal(file)
   if gp==msg[:len(gp)]:    
      messagebox.showinfo("Secret message is",msg[len(gp):])
   else:
      msg="Incorrect password cannot decode"
      #messagebox.showinfo("info",msg)
      #messagebox.showwarning("showwarning",msg)
      messagebox.showerror("ERROR", msg)
      


b1=Button(root,
          padx=5,
          pady=5,
          width=240,
          borderwidth=0,
          highlightthickness=-0.5,
          bg='DodgerBlue1',
          fg='white',
          relief=FLAT,
          command=encode,
          text='Encode',
          font=('helvetica 15 bold'),
          activebackground='light green'
          )
##img=PhotoImage(file="4.png")
##b1.config(image=img)
b1.place(x=190,y=145)


b2=Button(root,
          padx=5,
          pady=5,
          width=228,
          borderwidth=0,
          highlightthickness=0,
          bg='DodgerBlue1',
          fg='white',
          relief=FLAT,
          command=decode,
          text='Decode',
          font=('helvetica 15 bold'),
          activebackground='light green'
          )
##img2=PhotoImage(file="5.png")
##b2.config(image=img2)
b2.place(x=191,y=250)


root.mainloop()
