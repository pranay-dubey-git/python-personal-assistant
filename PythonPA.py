import speech_recognition as sr
import os
import sys
import re
import webbrowser
import requests
import subprocess
from pyowm import OWM
import youtube_dl
import pyttsx3
import urllib
import urllib3
import json
import bs4
from bs4 import BeautifulSoup as soup
from urllib3 import PoolManager
import csv 
import wikipedia
#import random
from time import strftime
from GoogleNews import GoogleNews
import pytube
beep = lambda x: os.system("echo -n '\a';sleep 0.1;" * x)
import pafy
import pyfiglet
import syslog
import time


voiceEngine = pyttsx3.init()
rate = voiceEngine.getProperty('rate')
volume = voiceEngine.getProperty('volume')
voices = voiceEngine.getProperty('voices')
voiceEngine.setProperty('rate',150)

def sofiaResponse(audio):
    "speaks audio passed as argument"
    print(audio)
    #print("mouth speak...")
    voiceEngine.say(audio)
    voiceEngine.runAndWait()
    


def myCommand():
    "listens for commands"
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        beep(2)
        command = r.recognize_google(audio).lower()
        #command= input("say something: ")
        voiceEngine.say(command)
        voiceEngine.runAndWait()
        print('You said: ' + command + '\n')
        beep(1)
    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('try again')
        beep(2)
        command = myCommand();
    return command






def assistant(command):
    "if statements for executing commands"
#open website
    if 'shutdown' in command:
        sofiaResponse('Bye bye Sir. Have a nice day')
        sys.exit()
    elif 'open' in command:
        reg_ex = re.search('open (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            print(domain)
            url = 'https://www.' + domain + '.com'
            webbrowser.open(url)
            sofiaResponse('The website you have requested has been opened for you Sir.')
    
#greetings
    elif 'hello' in command:
        day_time = int(strftime('%H'))
        if day_time < 12:
            sofiaResponse('Hello Sir. Good morning')
        elif 12 <= day_time < 17:
            sofiaResponse('Hello Sir. Good afternoon')
        else:
            sofiaResponse('Hello Sir. Good evening')
    elif 'help' in command:
        sofiaResponse("""
        You can use these commands and I'll help you out:
        1. Open xyz.com : replace xyz with any website name
        2. Current weather in {cityname} : Tells you the current condition and temperture
        3. hello
        4. news for today : reads top news of today
        5. time : Current system time
        6. tell me about xyz : tells you about xyz
        """)
#joke
    elif 'joke' in command:
        res = requests.get(
                'https://icanhazdadjoke.com/',
                headers={"Accept":"application/json"})
        if res.status_code == requests.codes.ok:
            sofiaResponse(str(res.json()['joke']))
        else:
            sofiaResponse('oops!I ran out of jokes')
#top stories from google news
    elif 'news for today' in command:
        try:
            http = urllib3.PoolManager()
            #news_url='https://www.indiatoday.in/news'
            Client=http.request('GET','https://www.indiatoday.in/news')
            #Client.data
            xml_page=Client.read()
            Client.close()
            soup_page=soup(xml_page,"xml")
            news_list=soup_page.findAll("item")
            for news in news_list[:15]:
                sofiaResponse(news.title.text.encode('utf-8'))
        except Exception as e:
                print(e)

#current weather
    elif 'current weather' in command:
        reg_ex = re.search('current weather in (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            owm = OWM(API_key='ab0d5e80e8dafb2cb81fa9e82431c1fa')
            obs = owm.weather_at_place(city)
            w = obs.get_weather()
            k = w.get_status()
            x = w.get_temperature(unit='celsius')
            sofiaResponse('Current weather in %s is %s. The max temperature is %0.2f degree celcius and the minimum temperature is %0.2f degree celcius' % (city, k, x['temp_max'], x['temp_min']))
#time
    elif 'time' in command:
        import datetime
        now = datetime.datetime.now()
        sofiaResponse('Current time is %d hours %d minutes' % (now.hour, now.minute))

   
#play youtube song
    elif 'play me a song' in command:
        path = '/home/pranay-dubey/Documents/videos/'
        folder = path
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        sofiaResponse('What song shall I play Sir?')
        mysong = myCommand()
        if mysong:
            flag = 0
            durl = "https://www.youtube.com/results?search_query=" + mysong.replace(' ', '+')
            r=urllib3.PoolManager()
            response = r.request('GET',durl)
            #html = response.read()
            soup1 = soup(response,"lxml")
            #url_list = [0]
            for vid in soup1.findAll(attrs={'class':'yt-uix-tile-link'}):
                if ('https://www.youtube.com' + vid['href']).startswith("https://www.youtube.com/watch?v="):
                    flag = 1
                    final_url = 'https://www.youtube.com' + vid['href']
                    url_list.append(final_url)
           # url = url_list[0]
            ydl_opts = {}
            os.chdir(path)
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                     ydl.download([durl])
                     vlc.play(path)
            if flag == 0:
                       sofiaResponse('I have not found anything in Youtube ')

    
#askme anything
    elif 'google search' in command:
         try:
            sofiaResponse('what should i google?')
            value= myCommand()
            #print("                      ")
            #wikipedia.set_lang(en)
            sofiaResponse(wikipedia.summary(value,sentences=15))
            sofiaResponse("              ")
         except Exception as e:
            print(e)
            sofiaResponse(e)
   
#loop to continue executing multiple commands
while True:
    assistant(myCommand())
    
