# Kalojen tunnistuksen käyttöliittymä

Huikea GUI, joka tunnistaa suomalaisia kaloja kuvan perusteella. Lajeina ahven, kuore, lahna ja muikku.

## Aloitus

Näillä ohjeilla pääset tykittelemään!

### Esivaatimukset

Pakollinen asennettava on
- [Python 3.X](https://www.python.org/downloads/). Käytin itse versiota 3.9.5.


### Asennus


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

Aja ohjelma fish_gui.py. Voit valita käyttää tallennettuja kuvia (kansiossa kuvat) tai näyttää printattuja kuvia web-kameralle. Painamalla Tunnista-nappia, käyttöliittymä avaa uuden ikkunan, jonka nimenä on tunnistuksen tulos.

Opetettu malli on kansiossa bs_12_epochs_100
