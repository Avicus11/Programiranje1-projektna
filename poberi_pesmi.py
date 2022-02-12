import requests

url = 'https://en.wikipedia.org/wiki/List_of_Eurovision_Song_Contest_winners'
response = requests.get(url)
vsebina = response.text
with open('evrovizija.html', 'w', encoding='utf-8') as dat:
    dat.write(vsebina)