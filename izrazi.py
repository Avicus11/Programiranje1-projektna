import pandas as pd
import re
import requests

url = "https://en.wikipedia.org/wiki/List_of_Eurovision_Song_Contest_winners"
vsebina = requests.get(url).text

def poisci_dolzino_skladbe(ime_skladbe):
	#Prenesi wikipedia stran o skladbi
	url_skladbe = poisci_url_skladbe(ime_skladbe)
	podatki_o_skladbi = requests.get(url_skladbe).text

	#Zajemi dolzino skladbe v minutah in sekundah
	vzorec = re.compile(
		r'<span class="min">(?P<minute>.+?)<\/span>.+?'
		r'<span class="s">(?P<sekunde>.+?)<\/span>',
		flags=re.DOTALL
	)

	#Ce stran vsebuje informacijo o dolzini, jo vrni, sicer vrni "Unknown"
	try:
		trajanje = vzorec.search(podatki_o_skladbi).groupdict()
	except:
		return "Unknown"
	return "{min}:{s}".format(min=trajanje['minute'], s=trajanje['sekunde'])

def poisci_url_skladbe(ime_skladbe):
	#Zajemi URL do Wikipedia strani skladbe
	vzorec = re.compile(r'href="(.+?)" title="(.+?)>{naslov}'.format(naslov=ime_skladbe));
	ujemanje = vzorec.search(vsebina)
	url_skladbe = "https://en.wikipedia.org{skladba}".format(skladba=ujemanje.group(1))
	return url_skladbe

#Prenesi tabelo
tabela = pd.read_html(url)[0] # Preberi prvo tabelo

#Odstrani nevaljaven stolpec
tabela = tabela.iloc[:, :-1]

#Odstrani wikipedijine hiperlinke z opombami
tabela = tabela.applymap(lambda x:re.sub('\[.+?\]', '', x))

#Odstrani narekovaje
tabela = tabela.applymap(lambda x:re.sub('"', '', x))

#Zapisi dolzine skladb
tabela.insert(loc=5, column='Song duration', value="Unknown")
for indeks, vrstica in tabela.iterrows():
	if(vrstica['Song']!='Contest cancelled due to the COVID-19 pandemic'):
		vrstica['Song duration'] = poisci_dolzino_skladbe(vrstica['Song'])


#Izpisi tabelo v csv datoteko
tabela.to_csv('tabela.csv', index=False)