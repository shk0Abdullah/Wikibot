from django.shortcuts import render, HttpResponse, redirect
import requests as r
import wikipedia
import re
import sys
import datetime
import json
# Create your views here.
from googletrans import Translator

YOURWEATHERAPI  = 'YOUR WHETHER API'
YOURNEWSAPI = 'YOUR NEWS API'

#list of all lang with lang codes
lang_list = {
            'Afrikaans' : 'af',
            'Albanian' : 'sq',
            'Amharic' : 'am',
            'Arabic' : 'ar',
            'Armenian' : 'hy',
            'Azerbaijani' : 'az',
            'Basque' : 'eu',
            'Belarusian' : 'be',
            'Bengali' : 'bn',
            'Bosnian' : 'bs',
            'Bulgarian' : 'bg',
            'Catalan' : 'ca',
            'Cebuano':'ceb',
            'Chichewa' : 'ny',
            'Chinese':'zh-CN',
            'Corsican' : 'co',
            'Croatian' : 'hr',
            'Czech' : 'cs',
            'Danish' : 'da',
            'Dutch' : 'nl',
            'English' : 'en',
            'Esperanto' : 'eo',
            'Estonian' : 'et',
            'Filipino' : 'tl',
            'Finnish' : 'fi',
            'French' : 'fr',
            'Frisian' : 'fy',
            'Galician' : 'gl',
            'Georgian' : 'ka',
            'German' : 'de',
            'Greek' : 'el',
            'Gujarati' : 'gu',
            'Haitian Creole' : 'ht',
            'Hausa' : 'ha',
            'Hawaiian ':'haw',
            'Hebrew' : 'he',
            'Hindi' : 'hi',
            'Hmong ' : 'hmn',
            'Hungarian' : 'hu',
            'Icelandic' : 'is',
            'Igbo' : 'ig',
            'Indonesian' : 'id',
            'Irish' : 'ga',
            'Italian' : 'it',
            'Japanese' : 'ja',
            'Javanese' : 'jw',
            'Kannada' : 'kn',
            'Kazakh' : 'kk',
            'Khmer' : 'km',
            'Kinyarwanda' : 'rw',
            'Korean' : 'ko',
            'Kurdish' : 'ku',
            'Kyrgyz' : 'ky',
            'Lao' : 'lo',
            'Latin' : 'la',
            'Latvian' : 'lv',
            'Lithuanian' : 'lt',
            'Luxembourgish' : 'lb',
            'Macedonian' : 'mk',
            'Malagasy' : 'mg',
            'Malay' : 'ms',
            'Malayalam' : 'ml',
            'Maltese' : 'mt',
            'Maori' : 'mi',
            'Marathi' : 'mr',
            'Mongolian' : 'mn',
            'Myanmar ' : 'my',
            'Nepali' : 'ne',
            'Norwegian' : 'no',
            'Odia' : 'or',
            'Pashto' : 'ps',
            'Persian' : 'fa',
            'Polish' : 'pl',
            'Portuguese' : 'pt',
            'Punjabi' : 'pa',
            'Romanian' : 'ro',
            'Russian' : 'ru',
            'Samoan' : 'sm',
            'Scots Gaelic' : 'gd',
            'Serbian' : 'sr',
            'Sesotho' : 'st',
            'Shona' : 'sn',
            'Sindhi' : 'sd',
            'Sinhala' : 'si',
            'Slovak' : 'sk',
            'Slovenian': 'sl',
            'Somali' : 'so',
            'Spanish': 'es',
            'Sundanese': 'su',
            'Swahili ': 'sw',
            'Swedish' : 'sv',
            'Tajik' : 'tg',
            'Tamil' : 'ta',
            'Tatar ': 'tt',
            'Telugu' : 'te',
            'Thai ': 'th',
            'Turkish ': 'tr',
            'Turkmen' : 'tk',
            'Ukrainian ': 'uk',
            'Urdu' : 'ur',
            'Uyghur' : 'ug',
            'Uzbek' : 'uz',
            'Vietnamese' : 'vi',
            'Welsh' : 'cy',
            'Xhosa' : 'xh',
            'Yiddish' : 'yi',
            'Yoruba' : 'yo',
            'Zulu' : 'zu',
            }



# Create your views here.
def translate(query,lang):

    # Initialize the translator
    translator = Translator()

    # Detect language
    text = query
    lang = lang_list[lang]
    detected = translator.detect(text)
    detected_language = detected.lang
    # out_lang = input("Which Language you'd like to translate: ")
    # lang = 'ar' #lang_list[out_lang.title()]
    # Translate text
    translated = translator.translate(text, dest=lang)
    return translated.text
def trans(query,lang):
    try:
        match = re.search(r'.* translate it: (.+) to (.+)',query)
        if match:
            text = match.group(1)
            lang = match.group(2)
            return translate(text, lang.title())
    except:
        pass

def index(request):
    return render(request, 'index.html')

def weather(query):
    try:
        api = YOURWEATHERAPI 
        weatherreport = re.search(r'.* temperature in (.+)',query)
        if weatherreport:
            city = weatherreport.group(1).capitalize()
            url = f"https://api.weatherapi.com/v1/current.json?key={api}&q={city}"
            response = r.get(url)
            temp = int(response.json()['current']['temp_c'])
            temp_f = int(response.json()['current']['temp_f'])            
            if 'fahrenheit' in query:
                return(f'{temp_f} degree fahrenheit')
            else:
                return(f'{temp} degree celsious')
    except:
        pass

def time(query):
    try:
        check = re.search(r'.* time', query)
        if check:
            time = datetime.datetime.now().strftime("%I:%M %p")
            return(f'Its {time}')
    except:
        pass

def wiki(query):
    try:
        match = re.search(r'.* about (.+)', query)
        if match:
            topic = match.group(1)
            try:
                return(wikipedia.summary(topic,sentences = 2))
            except:
                response = wikipedia.search(topic, results = 5)
                return(wikipedia.summary(response[0],sentences = 2))
    except:
        pass



def news(query):
    try:
        text = query
        api = YOURNEWSAPI
        match = re.search(r".+ news .+ about (.+)", text)
        topic = match.group(1)
        url = f'https://newsapi.org/v2/everything?q={topic}&sortBy=popularity&apiKey={api}'
        response = r.get(url)
        news = json.loads(response.text)
        i = 0
        pattern = r'\s*\[\+\d+ chars\]$'
        for article in news['articles']:
            if i == 0:
                speak.Speak(re.sub(pattern, '',article['content']))
            elif i == 3:
                raise ValueError
            else:
                return('Another Ariticle says', re.sub(pattern, '',article['content'])) 
            i += 1
    except:
        pass


def chat1(request):
    if request.method == 'GET':
        return render(request, 'chat.html')
    if request.method == 'POST':
        if 'conversation' not in request.session:
            request.session['conversation'] = []
        lang = ''
        query = request.POST.get('input_text')
        if time(query) != None:
            response = (time(query))
        elif 'clear' in query.lower().strip():
            request.session.clear()
            return render(request, 'chat.html')
        elif weather(query) != None:
            response = (weather(query))
        elif wiki(query) != None:
            response = (wiki(query))
        elif trans(query,lang) != None:
            response = (trans(query,lang))
        elif news(query) != None:
            response = (news(query))
        try:
            if query != None and response != None:
                request.session['conversation'].append({'user': query, 'bot': response})
                request.session.modified = True
            else:
                raise ValueError
        except:
            response = "Didn't understand! Try again"
            request.session['conversation'].append({'user': query, 'bot': response})
            request.session.modified = True
            
        return render(request, 'chat.html', {'conversation': request.session['conversation']})
