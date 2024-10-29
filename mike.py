from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import wikipedia
import webbrowser
import datetime
import subprocess
from ecapture import ecapture as ec
import wolframalpha
import requests
import pywhatkit
import pyjokes




# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend origin like http://localhost:5500
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/command")
def assist(command: str):
    command = command.lower()

    if "goodbye" in command or "stop" in command:
        return "Your personal assistant Mike is shutting down, Goodbye!"

    elif 'wikipedia' in command:
        command = command.replace("wikipedia", "")
        results = wikipedia.summary(command, sentences=3)
        return f"According to Wikipedia: {results}"

    elif 'open youtube' in command:
        webbrowser.open_new_tab("https://www.youtube.com")
        return "YouTube is open now."

    elif 'open google' in command:
        webbrowser.open_new_tab("https://www.google.com")
        return "Google is open now."

    elif 'open gmail' in command:
        webbrowser.open_new_tab("https://gmail.com")
        return "Gmail is open now."

    elif "weather" in command:
        api_key = "8ef61edcf1c576d65d836254e11ea420"
        city_name = command.split("in")[-1].strip()
        complete_url = f"https://api.openweathermap.org/data/2.5/weather?appid={api_key}&q={city_name}"
        response = requests.get(complete_url)
        x = response.json()
        if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"]
            current_humidity = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            return (f"Temperature: {current_temperature}K\n"
                    f"Humidity: {current_humidity}%\n"
                    f"Description: {weather_description}")
        else:
            return "City not found."

    elif 'time' in command:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        return f"The time is {strTime}"

    elif 'who are you' in command or 'what can you do' in command:
        return ('I am Mike, your personal assistant. '
                'I can open YouTube, Google, Gmail, check weather, play music, tell jokes, and more.')

    elif "who made you" in command:
        return "I was built by Mahesh."

    elif "open stackoverflow" in command:
        webbrowser.open_new_tab("https://stackoverflow.com/login")
        return "StackOverflow is open now."

    elif 'news' in command:
        webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
        return "Times of India is open now."

    elif "camera" in command or "take a photo" in command:
        ec.capture(0, "Mike Camera", "img.jpg")
        return "Photo taken."

    elif 'play' in command:
        song = command.replace('play', '')
        pywhatkit.playonyt(song)
        return f"Playing {song} on YouTube."

    elif 'ask' in command:
        question = command.replace('ask', '').strip()
        app_id = "R2K75H-7ELALHR35X"
        client = wolframalpha.Client(app_id)
        res = client.query(question)
        answer = next(res.results).text
        return f"The answer is: {answer}"

    elif 'joke' in command:
        joke = pyjokes.get_joke()
        return joke

    return "Command not recognized."


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
