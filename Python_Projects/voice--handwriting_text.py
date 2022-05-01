import pywhatkit as pwk
import speech_recognition as sr
def take_voice():
    r = sr.Recognizer()
    with sr.Microphone() as word:
        print("listening...")
        audio = r.listen(word)
    try:
        print("Recognize...")
        query = r.recognize_google(audio,language='en-us')
        print(query)
    except Exception as e:
        print("speech again")
        return "none"
    return query
query = take_voice().casefold()
pwk.text_to_handwriting(query ,"C:\\Users\\Shyam Patel\\Desktop\\sp.png",[200,0,20])
# pwk.text_to_handwriting(ch,"C:\\Users\\Shyam Patel\\OneDrive\\Desktop\\sp.png",[0,0,20])
