
## Forklaring av moduler

ConfigManager er en klasse som håndterer konfigurasjonen til programmet. 
Den leser inn en konfigurasjonsfil og setter opp alle variabler som trengs for å kjøre programmet. 
Denne klassen er initialisert i main.py og blir brukt av alle andre klasser som trenger tilgang til konfigurasjonen.

ImportManager er en klasse som håndterer importering av data. Den leser inn filene som ligger inni mappen import 
Han leser filene som i .tar format og pakker de ut, og omformer objekter til placeholderer som deretter brukes av 
andre klasser til å legge inn data. Filene som han importerer lagrer han i en mappe som heter schematics og de er i 
.yml format. Han bruker databasen til å samenligne dataene som er i filene med dataene som er i databasen til å lage 
placeholderer for å få det til å fungere databasen må være tilgjengelig og i config.yml må ha specifisert hvilke 
objekter skal brukes. 

InfoWidgetFactory er en klasse som lager widgets som viser informasjon om et rom. Denne klassen er initialisert i main 
og bruker schematikker som er lagret i schematics mappen. Det må specifiseres hvilken schematic han skal bruke inni 
config.yml fil. Han bruker databasen til å finne ut hvilke objekter som skal brukes. Ferdige widgets blir lagret i
mappen output og er i .tar format. De kan importeres til LM uten å måtte endre på noe. 

TrendWidgetFactory er en klasse som lager widgets som viser trender for et rom. Denne klassen er initialisert i main
og bruker schematikker som er lagret i schematics mappen. Det må specifiseres hvilken schematic han skal bruke inni
config.yml fil. Han bruker databasen til å finne ut hvilke trender som skal brukes. Ferdige widgets blir lagret i
mappen output og er i .tar format. De kan importeres til LM uten å måtte endre på noe. 

Alt henger sammen i main som er hovedklassen og som initialiserer alle andre klasser. Denne klassen er også ansvarlig
for å kjøre programmet i riktig rekkefølge. Og den lager mapper og installerer moduler som kan ikke eksistere i 
lokal interpreter. 

## Hvordan kjøre programmet









