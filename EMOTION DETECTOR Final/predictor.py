import joblib
import tkinter as tk
gnb = joblib.load("model.pkl")
def emopred(X):
    Y= gnb.predict(X)
    return Y

fields = ('Systolic Pressure','Diastolic Pressure', 'Heart Rate', 'Pulse Rate', 'Blood Viscosity', 'Emotion')
def Emotion(entries):
    # period rate:
    sys = float(entries['Systolic Pressure'].get()) 
    dia =float(entries['Diastolic Pressure'].get())
    har =float(entries['Heart Rate'].get())
    pul =float(entries['Pulse Rate'].get())
    bv=float(entries['Blood Viscosity'].get())
    X=[[sys,dia,har,pul,bv]]
    y=emopred(X)
    if y==0:
        emo='Angry'
    elif y==1:
        emo='Depressed'
    elif y==3:
        emo='Sad'
    elif y==4:
        emo='Stressed'
    else:
        emo='Happy'
    entries['Emotion'].delete(0, tk.END)
    entries['Emotion'].insert(0, emo )
def exit():
    root.destroy()
def makeform(root, fields):
    entries = {}
    for field in fields:
        print(field)
        row = tk.Frame(root)
        if field!='Emotion':
            lab = tk.Label(row,bg='#F7D8D8',font=('times', 15, 'italic'), width=20, text=field+"", anchor='w')
            ent = tk.Entry(row,font=('times', 15, 'italic'))
            ent.insert(0, "0")
        else:
            lab = tk.Label(row,bg='#F7D8D8',font=('times', 15, 'italic'), width=20, text=field+"", anchor='w')
            ent = tk.Entry(row,font=('times', 15, 'italic'))
            ent.insert(0, "")
        row.pack(side=tk.TOP, 
                 fill=tk.X, 
                 padx=10, 
                 pady=10)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, 
                 expand=tk.YES, 
                 fill=tk.X)
        entries[field] = ent
    return entries

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Machine Learning Based Human Emotion Recognition using variations in Biological Parameters")
    root.config(bg='#A0A0A0')
    msg = tk.Message(root, text = 'Emotion \tDetector')
    msg.config(bg='lightblue', font=('times', 19, 'italic'),aspect=200
               )
    msg.pack(side=tk.TOP, padx=100, pady=20)
    ents = makeform(root, fields)
    b1 = tk.Button(root, text='Find Emotion',bg='lightgreen',font=('times', 15, 'italic'),
           command=(lambda e=ents: Emotion(e)))
    b1.pack(side=tk.LEFT, padx=80, pady=5)
    b2 = tk.Button(root, text='Quit',bg='red',font=('times', 15, 'italic'),command=exit)
    b2.pack(side=tk.RIGHT, padx=100, pady=5)
    root.mainloop()
        

