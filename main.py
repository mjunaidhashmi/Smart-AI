import speech_recognition as sr
import webbrowser
from openai import OpenAI
from gtts import gTTS
import requests
import os
import pygame
import random

# Initialize recognizer
r = sr.Recognizer()

# Speak function using gTTS and pygame
def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")

# Main command processor
def processCommand(command):
    command = command.lower()
    
    # Common website commands
    if "open google" in command:
        webbrowser.open("https://google.com")
    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in command:
        webbrowser.open("https://linkedin.com")
    elif "open insta" in command:
        webbrowser.open("https://instagram.com")
    
    # News fetching using NewsAPI
    elif "news" in command:
        newsapi = "newsapi"
        url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                if articles:
                    article = random.choice(articles)
                    speak(article.get("title", "No title available."))
                else:
                    speak("No news articles found.")
            else:
                speak("Failed to fetch news.")
        except Exception as e:
            speak("Error getting news.")
            print(f"News Error: {e}")
    
    # Default fallback to OpenAI
    else:
        try:
            client = OpenAI(api_key="openai apikey")  
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "you are my ai assisstent called jarvis answer to my questions plus rrequest and make em short pls"},
                    {"role": "user", "content": command}
                ]
            )
            result = completion.choices[0].message.content
            speak(result)
        except Exception as e:
            speak("put in apikey")
            print(f"OpenAI Error: {e}")

# MAIN FUNCTION
if __name__ == "__main__":
    speak("Initializing Jarvis...")

    
    while True:
        print("SAY MY NAME")
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening....")
                audio = r.listen(source, timeout=5, phrase_time_limit=4)
                word = r.recognize_google(audio)
                print(f"DETECTED WORD: {word}")
                if "jarvis" in word.lower():
                    speak("what is it")
                    break
        except sr.UnknownValueError:
            continue
        except sr.WaitTimeoutError:
            continue

    while True:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.3)
                audio = r.listen(source, timeout=4, phrase_time_limit=6)
                command = r.recognize_google(audio)
                print(f"COMMAND: {command}")
                if command.lower()=="deactivate":
                    break
                processCommand(command)

        except sr.UnknownValueError:
            speak("Speak clearly please")
        except sr.WaitTimeoutError:
            speak("Say something")
        except Exception as e:
            speak("Unexpected error occurred.")
            print(f"General Error: {e}")