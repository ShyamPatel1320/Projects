import pyttsx3
from datetime import datetime
import holidays
import calendar
import wikipedia
import webbrowser
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices',voices[1].id)
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
def table(num):
    for i in range(1,11):
        print(num, '*' ,i, '=' , num*i )
def game():
    import random
    lst=["snake","water","gun"]
    x=1
    cp1=0
    cp2=0
    print(":--10 points game--:")
    while x<=10:
        p1=random.choice(lst)
        p2=input("enter your choice(snake,water,gun)  :")
        print(f"your choice--{p2}\ncomputer choice--{p1}")
        if p1=="snake":
            if p2=="water":
                cp1+=1
            elif p2=="gun":
                cp2+=1
            elif p2=="snake":
                print("same reactions")
            else:
                print("wrong entry")
        elif p1=="water":
            if p2=="gun":
                cp1+=1
            elif p2=="snake":
                cp2+=1
            elif p2=="water":
                print("same reactions")
            else:
                print("wrong entry")
        elif p1=="gun":
            if p2=="snake":
                cp1+=1
            elif p2=="water":
                cp2+=1
            elif p2=="gun":
                print("same reactions")
            else:
                print("wrong entry")
        else:
            print("wrong entry")
        x+=1
    print("\nMATCH END")
    print("\nYour score:",cp2)
    print("\nComputer score",cp1)
    if cp1==cp2:
        print("Game Tie")
    elif cp1>cp2:
        print("\nYou lose")
    else:
        print("\nYou win")

if __name__ == '__main__':            
    while True:
        ch = input("Type here : ").lower()
        if "hello" in ch:
            print("-----------------------------------------------------------------")
            print("hello sir")
            speak("hello sir")
            print("-----------------------------------------------------------------")
            now = datetime.now()
            #current_time = now.strftime("time = %H:%M:%S:    date = %d:%m:%Y")
            if int(now.strftime("%H"))>6 and int(now.strftime("%H"))<12:
                print("Good morning sir")
                speak("Good morning sir")
                print("-----------------------------------------------------------------")
            elif int(now.strftime("%H"))>12 and int(now.strftime("%H"))<18:
                print("Good afternoon sir")
                speak("Good afternoon sir")
                print("-----------------------------------------------------------------")
            elif int(now.strftime("%H"))>18 and int(now.strftime("%H"))<21:
                print("Good evening sir")
                speak("Good evening sir")
                print("-----------------------------------------------------------------")
        elif ("time" or "date") in ch:
            now = datetime.now()
            current_time = now.strftime("current time = %H:%M:%S \n and Date = %d %B %Y")
            print("-----------------------------------------------------------------")
            print("Current Time : ", current_time)
            speak(current_time)
            print("-----------------------------------------------------------------")
        elif "your name" in ch:
            print("-----------------------------------------------------------------")
            print("I am Python compiler")
            speak("I am Python compiler")
            print("-----------------------------------------------------------------")
            speak("What is your name :")
            uname = input("What is your name :")
            print("-----------------------------------------------------------------")
            print(uname)
            speak(uname)
            print("-----------------------------------------------------------------")
            print("Nice sir")
            speak("Nice Name sir")
        elif "are you from" in ch:
            print("-----------------------------------------------------------------")
            print("I am from computer world!!")
            speak("I am from computer world!!")
            print("-----------------------------------------------------------------")
            speak("Where are you from :")
            ucountry = input("Where are you from :")
            print("-----------------------------------------------------------------")
            print(ucountry)
            speak(ucountry)
            print("-----------------------------------------------------------------")
            print("Nice country")
            speak("Nice country")
            print("-----------------------------------------------------------------")
        elif "do for me" in ch:
            print("-----------------------------------------------------------------")
            print("I am doing anything for you what you want :)")
            speak("I am doing anything for you what you want :)")
            print("-----------------------------------------------------------------")
            speak("you need any help : ")
            uhelp = input("you need any help : ")
            print("-----------------------------------------------------------------")
            continue
        elif "+" in ch:
            ans = int(ch.split('+')[0]) + int(ch.split('+')[1])
            print(ans)
            speak(ans)
        elif "-" in ch:
            ans = int(ch.split('-')[0]) - int(ch.split('-')[1])
            print(ans)
            speak(ans)
        elif "*" in ch:
            ans = int(ch.split('*')[0]) * int(ch.split('*')[1])
            print(ans)
            speak(ans)
        elif "/" in ch:
            ans = int(ch.split('/')[0]) / int(ch.split('/')[1])
            print(ans)
            speak(ans)
        elif "table of" in ch:
            num = int(ch[-1:])
            table(num)
        elif "play game" in ch:
            game()
        elif "holiday" in ch:
            date = "%d:%m:%Y"
            ind_holiday = holidays.IND()
            for date,name in sorted(holidays.India(years=2021).items()):
                print(date,name)
        elif "calendar" in ch:
            yy = datetime.today().year
            mm = datetime.today().month
            print(calendar.month(yy,mm))
        elif 'youtube' in ch:
            speak("opening youtube")
            webbrowser.open("www.youtube.com")
        elif 'google' in ch:
            speak("opening google")
            webbrowser.open("www.google.com")
        elif 'microsoft edge' in ch:
            speak("opening microsoft edge")
            webbrowser.open("microsoft edge.com")  
        elif 'wikipedia' in ch:
            speak("searching wikipedia....")
            ch = ch.replace("wikipedia","")
            result=wikipedia.summary(ch,sentences=2)
            print(result)
            speak(result)
        elif "bye" in ch:
            break
    print("okay , bye sir")
    speak("okay , bye sir")
    if int(now.strftime("%H"))>22:
        print("Good night sir")
        speak("Good night sir")