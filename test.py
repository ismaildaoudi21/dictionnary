import requests
import os
from urllib.parse import quote

def lookup(word):
    api_key = os.environ.get("API_KEY")
    url = f"https://owlbot.info/api/v4/dictionary/{word}"
    headers = {"content-type": "application/json", 'Authorization':'Token ' + api_key}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()
    return {
            "word": data["word"],
            "pronunciation": data["pronunciation"],
            "definitions": data["definitions"],
        }

def lookup_image(word):
    api_key_pixabay = os.environ.get("API_KEY_image")
    url = "https://pixabay.com/api/?key="+api_key_pixabay+"&q="+quote(word)
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    return data

results = lookup_image('cars')
for elt in results['hits']:
    print(elt['webformatURL'])