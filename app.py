import speech_recognition as sr
import pyttsx3
import requests
import pygame
import time
import os

# Text-to-speech
engine = pyttsx3.init()
def speak(text):
    print(f"🤖: {text}")
    engine.say(text)
    engine.runAndWait()

# Play intro sound using pygame
def play_intro_sound():
    try:
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("intro.mp3")  # Ensure this file exists
        pygame.mixer.music.play()
        time.sleep(3)  # Adjust duration as needed
        pygame.mixer.music.stop()
    except Exception as e:
        print("🔇 Intro sound play nahi hua:", e)

# Speech-to-text
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Bol bhai...")
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language="en-IN")
        print(f"👦: {query}")
        return query.lower()
    except:
        speak("Sorry bhai, samajh nahi aaya.")
        return ""

# Typing input
def type_input():
    query = input("⌨️  Type karo bhai: ")
    print(f"👦: {query}")
    return query.lower()

# Weather API function
def get_weather(city):
    api_key = "3ca77b989f6a547048b86c9bfebb467e"  # <-- Teri API key
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        res = requests.get(url)
        data = res.json()

        if data["cod"] != 200:
            return f"City '{city}' nahi mila bhai."

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"{city} mein temperature hai {temp}°C aur weather hai '{desc}'."
    except:
        return "Bhai kuch gadbad ho gayi weather laate waqt."

# OpenRouter GPT response
def get_ai_response(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": "Bearer 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",  # <-- OpenRouter API Key
        "Content-Type": "application/json"
    }
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "Tum ek helpful aur friendly Hindi assistant ho."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        data = res.json()
        reply = data["choices"][0]["message"]["content"]
        return reply.strip()
    except Exception as e:
        return "AI se jawab laate waqt kuch error aaya bhai."

# Main loop
def main():
    play_intro_sound()
    speak("Namastey! Main hoon Desi Siri.")

    # Choose input mode
    speak("Mic se baat karni hai ya keyboard se? (bolo 'mic' ya 'type')")
    mode = input("🔵 Mic ya Type? (mic/type): ").strip().lower()

    if mode == "mic":
        input_method = listen
    else:
        input_method = type_input

    while True:
        query = input_method()

        if "weather" in query:
            speak("Kaun se city ka weather chahiye bhai?")
            city = input_method()
            if city:
                report = get_weather(city)
                speak(report)

        elif "band kar" in query or "exit" in query:
            speak("Bye bhai, milte hain phir.")
            break

        elif query:
            response = get_ai_response(query)
            speak(response)

if __name__ == "__main__":
    main()
