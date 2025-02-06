import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import requests
import random
import subprocess
import wikipedia
import json

# Voice Assistant Name: Lana
# Created by Manas Pandey

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty('rate', 180)
engine.setProperty('voice', 'english')

def speak(text):
    """Converts text to speech"""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Captures voice input and converts it to text"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

def open_website(site):
    """Opens a website in the default browser"""
    webbrowser.open(f"https://{site}.com")
    speak(f"Opening {site}")

def tell_time():
    """Tells the current time"""
    now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {now}")

def search_wikipedia(query):
    """Searches Wikipedia and returns a summary"""
    try:
        result = wikipedia.summary(query, sentences=2)
        speak(result)
    except wikipedia.exceptions.DisambiguationError:
        speak("There are multiple results, please be more specific.")
    except wikipedia.exceptions.PageError:
        speak("No results found.")

def get_weather(city):
    """Fetches weather information using Open-Meteo API"""
    url = f"https://api.open-meteo.com/v1/forecast?latitude=35.6895&longitude=139.6917&current_weather=true"
    response = requests.get(url)
    weather_data = response.json()
    if weather_data.get("current_weather"):
        temp = weather_data['current_weather']['temperature']
        description = weather_data['current_weather']['weathercode']
        speak(f"The current temperature in {city} is {temp} degrees Celsius with condition code {description}.")
    else:
        speak("Unable to fetch weather details.")

def get_news():
    """Fetches the latest news using NewsAPI"""
    url = "https://newsdata.io/api/1/news?apikey=YOUR_FREE_API_KEY&country=in&language=en"
    response = requests.get(url)
    news_data = response.json()
    if "results" in news_data:
        top_articles = news_data["results"][:3]
        for article in top_articles:
            speak(article["title"])
    else:
        speak("Unable to fetch news.")

def roll_dice():
    """Rolls a dice and returns a random number"""
    result = random.randint(1, 6)
    speak(f"You rolled a {result}")

def open_github():
    """Opens GitHub"""
    webbrowser.open("https://github.com")
    speak("Opening GitHub")

def open_youtube():
    """Opens YouTube"""
    webbrowser.open("https://www.youtube.com")
    speak("Opening YouTube")

def shutdown_system():
    """Shuts down the system"""
    speak("Shutting down the system in 10 seconds. Save your work.")
    os.system("shutdown /s /t 10")

def main():
    speak("Hello! I am Lana, your personal assistant. How can I assist you today?")
    while True:
        command = listen()
        if "time" in command:
            tell_time()
        elif "open youtube" in command:
            open_youtube()
        elif "open github" in command:
            open_github()
        elif "open google" in command:
            open_website("google")
        elif "weather in" in command:
            city = command.split("in")[-1].strip()
            get_weather(city)
        elif "wikipedia" in command:
            query = command.replace("wikipedia", "").strip()
            search_wikipedia(query)
        elif "roll dice" in command:
            roll_dice()
        elif "shutdown system" in command:
            shutdown_system()
        elif "news" in command:
            get_news()
        elif "exit" in command or "quit" in command:
            speak("Goodbye!")
            break
        else:
            speak("I didn't understand that. Can you repeat?")

if __name__ == "__main__":
    main()
