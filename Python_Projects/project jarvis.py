import pyttsx3  
import datetime
import wikipedia
import webbrowser
import os
import speech_recognition as sr
import smtplib
engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voices',voices[1].id)
def speak(audio):
    '''it is for speak audio'''
    engine.say(audio)
    engine.runAndWait()
def wishme():
    '''it is wish us as current time'''
    hour=(datetime.datetime.now().hour)
    if hour>4 and hour<=12:
        speak("Good Morning Sir!")
    elif hour>12 and hour<18:
        speak("Good AfterNoon Sir!")
    elif hour>=18 and hour<21:
        speak("Good Evening Sir!")
    speak("How can i help you sir!")
def takevoice():
    ''' it is take our voice and racognize'''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold=1
        audio=r.listen(source)
    try:
        print("Recognize...")
        query = r.recognize_google(audio,language='en-in')
        print(query)
    except Exception as e:
        print(e)
        print("please tell me again")
        return "None"
    return query
def sendemail(to,content):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('your email','your password')
    server.sendmail('your email',to,content)
    server.close()

if __name__ == '__main__':
    speak("hello")
    wishme()
    while True:
        query=takevoice().lower()
        if 'wikipedia' in query:
            speak("searching wikipedia..")
            query = query.replace("wikipedia","")
            result=wikipedia.summary(query,sentences=2)
            speak("According to wikipedia")
            speak(result)
        elif 'how are you' in query:
            speak("i am fine Sir!")
        elif ' youtube' in query:
            speak('yes sir')
            webbrowser.open("www.youtube.com")
        elif ' google' in query:
            speak('yes sir')
            webbrowser.open("www.google.com")
        elif ' microsoft edge' in query:
            speak('yes sir')
            webbrowser.open("microsoft edge.com")    
        elif 'visual code' in query:
            speak('yes sir')
            path="C:\\Users\\Shyam Patel\\Microsoft VS Code\\Code.exe"
            os.startfile(path)
        elif 'send email' in query:
            try:
                speak("what is message you want to send")
                to = 'email@gmail.com'
                content=takevoice()
                sendemail(to,content)
                speak("your email has been sent")
            except Exception as ee:
                print(ee)
                speak("due to some error your email can not be send!")
        elif 'bye' in query:
            speak("bye sir")
            exit() 