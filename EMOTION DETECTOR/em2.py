from em1 import emopred
import win32com.client as wincl
speak = wincl.Dispatch("SAPI.SpVoice")
import shutil
print ("\n")
columns = shutil.get_terminal_size().columns
print("EMOTION DETECTOR".center(columns))
print ("\n")
print('Welcome to Emotion Detector Software')
speak.Speak('Welcome to Emotion Detector Software')
speak.Speak('Moving to the test')

count= 0
while (count<5):
    count=count+1
    

    print ("\n")
    print("Test no.",count)
    
    print("Enter your Systolic Pressure : ",)
    speak.Speak('Enter your Systolic Pressure ')
    sys = float(input())
       
    
    print("Enter your Diastolic Pressure :")
    speak.Speak('Enter your Diastolic Pressure')
    dia = float(input())

    print("Enter your Heart Rate :")   
    speak.Speak('Enter your Heart Rate')
    har = float(input())
    
    print("Enter your Pulse Rate :")
    speak.Speak('Enter your Pulse Rate ')
    pul = float(input())
    
    print("Enter your Blood Viscosity(0.2832 - 0.4260):")
    speak.Speak('Enter your Blood Viscosity ')
    bv = float(input())
    
    X=[[sys,dia,har,pul,bv]]
    print(X)
    print ("\n")  
    emopred(X)
    if emopred(X)==0:
        print("Your emotion is: Angry")
        print("CalmDown don't get angry")
        speak.Speak("CalmDown don't get angry")
    
    elif  emopred(X)==1:
        print("Your emotion is: Depressed")
        print('Dont get depressed We are with you')
        speak.Speak('Dont get depressed We are with you')
    elif emopred(X) ==2:
        print("Your emotion is: Happy")
        print('Looks like some one is happy ')
        speak.Speak('ohh!.Looks like some one is happy')
        
    elif  emopred(X)==3:
        print("Your emotion is: Sad")
        print('Dont be sad')
        speak.Speak('Dont be sad')
        
    elif  emopred(X)==4:
        print("Your emotion is: Stressed")
        print('Dont take toomuch pressure,take a break and meditate')
        speak.Speak('Dont take toomuch pressure,take a break and meditate')

    print ("\n")
    print("Are you satisfied (Y/N): ")
    speak.Speak("Are you satisfied ")
    f = input()
    
    print ("\n")
    if f== 'Y' or f=='y':
       print("Thank you")
       speak.Speak("Thank You, Take care ")
    elif f== 'n' or f== 'N':
        print("Sorry, I'm still learning")
        speak.Speak("Sorry. I'm still learning")
    else :
        print("thank you")
        speak.Speak("Thank you, Take care")
    speak.Speak('moving to new test')
