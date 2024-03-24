import warnings
import pyttsx3
import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import datetime
import calendar
import random
import webbrowser


warnings.filterwarnings("ignore")

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def talk(audio):
    engine.say(audio)
    engine.runAndWait()


def record():
    recog = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("Listening...")
        try:
            audio = recog.listen(source, timeout=5)  # Adjust timeout as needed
            data = recog.recognize_google(audio)
            print("You said:", data)
            return data
        except sr.WaitTimeoutError:
            print("Listening timed out.")
            return ""  # Return empty string if timeout occurs
        except sr.UnknownValueError:
            print("Unable to recognize your voice.")
            return ""
        except sr.RequestError as ex:
            print("Speech recognition request failed:", ex)
            return ""


def response(text):
    print("Encom:", text)
    tts = gTTS(text=text, lang='en')
    audio_file = "response.mp3"
    tts.save(audio_file)
    playsound.playsound(audio_file)
    os.remove(audio_file)


def greet(text):
    greetings = ["hi", "hello", "how are you", "hola", "hey whatsapp"]
    if any(word in text.lower() for word in greetings):
        return random.choice(greetings)
    return ""


def get_date():
    today = datetime.datetime.now()
    day = calendar.day_name[today.weekday()]
    month = calendar.month_name[today.month]
    ordinal = "th" if 11 <= today.day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(today.day % 10, "th")
    return f"Today is {day}, {month} {today.day}{ordinal}"

def flip_a_coin():
    return random.choice(['heads','tails'])
    
def reminder(reminder_text,reminder_time):
    try:
        reminder_time = datetime.datetime.strptime(reminder_time, "%H:%M")
        current_time = datetime.datetime.now().time()
        while True:
            current_time = datetime.datetime.now().time()
            if current_time >= reminder_time:
                talk(f"Reminder: {reminder_text}")
                break
    except ValueError:
        talk("Invalid time format. Please provide time in HH:MM format.")

while True:
    try:
        text = record()
        response_text = greet(text)

        if "date" in text or "day" in text or "month" in text:
            response_text += " " + get_date()

        elif "time" in text:
            now = datetime.datetime.now()
            meridiem = "PM" if now.hour >= 12 else "AM"
            response_text += f" It's {now.hour % 12}:{now.minute:02d} {meridiem}"

        elif "who are you " in text:
            response_text= response_text+""" I'm encom I was created in 2024"""

        elif "your name"  in text:
            response_text=response_text+" My name is encom"
        elif " how was your day" in text:
            response_text=response_text+" It was a good day How about yours"
        elif " flip a coin" in text:
            response_text=response_text+flip_a_coin()

        elif "reminder" in text:
            talk("What do you want me to remind you?")
            reminder_text = record()
            talk("At what time?")
            reminder_time = record()
            reminder(reminder_text, reminder_time)


        elif "open" in text.lower():
            if "google" in text.lower():
                response_text= response_text+"opening google"
                os.startfile("https://www.google.com")

            if "youtube" in text.lower():
                response_text=response_text+"opening youtube"
                os.startfile("https://www.youtube.com/")

            if      



        if response_text:
            response(response_text)
    except Exception as e:
        print("An error occurred:", e)
        talk("I encountered an error. Please try again.")

