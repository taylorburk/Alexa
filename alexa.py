import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import requests
import wolframalpha
import webbrowser
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
 
listener = sr.Recognizer()
engine = pyttsx3.init('nsss')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[33].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def command1():
    r = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print("Alexa: Listening...")
            audio=r.listen(source)
            try:    
                command = r.recognize_google(audio)
                print(f"person:{command}")
                return command
                break
            except:
                print("Try Again")


def run_alexa():
    command = command1().lower()
    
    if 'alexa' in command:
        def wishMe():
            hour = int(datetime.datetime.now().hour)
            if hour>= 0 and hour<12:
                talk("Good Morning ! How can I help you today? ")
            elif hour>= 12 and hour<18:
                talk("Good Afternoon! How can I help you toady? ")  
            else:
                talk("Good Evening! How can I help you today?") 
        wishMe()

    elif 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)

    elif 'bye' in command:
        talk('Goodbye')
        exit()

    elif 'what time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)

    elif 'how are you' in command:
            talk("I am fine, Thank you")
            talk("How are you")
 
    elif 'fine' in command or "good" in command:
            talk("It's good to know that your fine")
 

    elif 'who' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, sentences=2, auto_suggest=False, redirect=True)
        print(info)
        talk(info)

    elif 'what is' in command:
        person = command.replace('what is', '')
        info = wikipedia.summary(person, sentences=2, auto_suggest=True, redirect=True)
        print(info)
        talk(info)

    elif 'on a date' in command:
        talk('sorry, I have a headache')

    elif 'are you single' in command:
        talk('I am in a relationship with wifi')

    elif 'thank you' in command:
        talk('You are welcome')

    elif 'joke' in command:
        talk(pyjokes.get_joke())

    elif 'news' in command:
            def trndnews(): 
                url = "http://newsapi.org/v2/top-headlines?country=in&apiKey=59ff055b7c754a10a1f8afb4583ef1ab"
                page = requests.get(url).json() 
                article = page["articles"] 
                results = [] 
                for ar in article: 
                    results.append(ar["title"]) 
                for i in range(len(results)): 
                    print(i + 1, results[i]) 
                talk("here are the top trending news....!!")
            trndnews() 

    elif 'open google and search' in command:
        reg_ex = re.search('open google and search (.*)', command)
        search_for = command.split("search",1)[1]
        url = 'https://www.google.com/'
        if reg_ex:
            subgoogle = reg_ex.group(1)
            url = url + 'r/' + subgoogle
        talk('Okay!')
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        s= Service('./chromedriver') 
        driver = webdriver.Chrome(service=s,options= chrome_options) 
        driver.get('http://www.google.com')
        search = driver.find_element(by=By.NAME, value='q') 
        search.send_keys(str(search_for)) #sends search keys 
        search.send_keys(Keys.RETURN) #hits enter

    elif "calculate" in command:
             
            app_id = "XTUPXK-J9575V2A93"
            client = wolframalpha.Client(app_id)
            indx = command.lower().split().index('calculate')
            query = command.split()[indx + 1:]
            res = client.query(' '.join(query))
            answer = next(res.results).text
            print("The answer is " + answer)
            talk("The answer is " + answer)

    elif "weather" in command:
            def weather(city):
                city = city.replace(" ", "+")
                res = requests.get(
                    f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
                print("Searching...\n")
                soup = BeautifulSoup(res.text, 'html.parser')
                location = soup.select('#wob_loc')[0].getText().strip()
                time = soup.select('#wob_dts')[0].getText().strip()
                info = soup.select('#wob_dc')[0].getText().strip()
                weather = soup.select('#wob_tm')[0].getText().strip()
                print(location)
                talk(location)
                print(time)
                talk(time)
                print(info)
                talk(info)
                print(weather+"°F")
                talk(weather+"°F")
            talk("Say the name of the City ")
            city_name=command1()
            city = city_name+" weather"
            weather(city)


    else:
        talk('please say the command again')
    

while True:
    run_alexa() 
