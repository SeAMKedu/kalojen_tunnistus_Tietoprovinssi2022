# Kalojen tunnistuksen käyttöliittymä

Tietoprovinssissa 2022 esitelty yksinkertainen graafinen käyttöliittymä, jonka avulla voidaan tunnistaa suomalaisia kaloja joko kovalevylle tallennettujen kuvien tai web-kameran perusteella. Lajeina ahven, lahna, kuore ja muikku. Taustalla toimii konvoluutioneuroverkko, jota on opetettu vajaalla sadalla samantyylisellä kuvalla kuin kuvat-kansiossa on. Kuvat-kansion kuvia ei ole käytetty neuroverkon opetuksessa, joten ne ovat puhtaasti testidataa. Kuva Iso-Lahna-kulma-44-0.jpeg tunnistu väärin ahvenena, muut tunnistuvat oikein. Kuvat-kansion kuvia voi tulostaa paperille ja näyttää niitä web-kameralle. Se on haasteellisempi tunnistustehtävä kuin pelkkien kuvien käyttö, sillä tällin kuvien orientaatio, värimaailma ja rajaus väkisinkin muuttuvat. Koska neuroverkon opetusdata on ollut rajallista, se tuskin tunnistaa esim. erivärisellä taustalla olevia kaloja.

Iso kiitos kalan kuvista Antti Kinnuselle XAMkista!

## Aloitus

Näillä ohjeilla saat ohjelman asennettua.

### Esivaatimukset

Pakollinen asennettava on
- [Python 3.X](https://www.python.org/downloads/). Käytin itse versiota 3.9.5.


### Asennus

Asennus onnistuu helpoimmin seuraavia askelia noudattamalla:

1. kloonaa repo
2. mene repokansioon
3. luo virtuaaliympäristö komennolla
```
<pythonin_polku>\python -m venv <virtuaaliympariston_nimi>
```
4. ota virtuaaliympäristö käyttöön (esim. VS Coden pitäisi ottaa se automaattisesti, mutta manuaalisesti saa painamalla Ctrl+Shift+p, hakemalla "Python interpreter", sieltä Select Interpreter -> luodun venv-kansion Scripts-kansiosta valitsee python.exen). Kun avaa uuden terminaalin VS Codessa, rivin edessä pitäisi nyt näkyä teksti (venv)
5. asenna riippuvuudet: 
```
pip install -r requirements.txt
```

## Käyttö

Aja ohjelma fish_gui.py. Voit valita käyttää tallennettuja kuvia (kansiossa kuvat) tai näyttää printattuja kuvia web-kameralle. Painamalla Tunnista-nappia, käyttöliittymä avaa uuden ikkunan, jonka nimenä on tunnistuksen tulos, esim. 'Kala on ahven'.

Opetettu konvoluutioneuroverkko on kansiossa bs_12_epochs_100. Käyttöliittymä lataa mallin tuosta kansiosta, joten kansiota ei saa siirtää muualle.
