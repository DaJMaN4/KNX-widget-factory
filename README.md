
## Forklaring av moduler

ImportManager er en klasse som håndterer importering av widgterer. Den leser inn filene som ligger inni mappen import 
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

### Hva kan det brukes til 
Dette kan brukes til å generere widgets som viser informasjon om et rom og widgets som viser trender for et rom.
Målsetningen er å gjøre det enkelt å lage widgeter som differ fra hverandre bare i objekter 

### Trend Widgets 

Denne modulen lager widgets som viser trender i en category. Han lager ikke categorier selv, for å gjøre det bruk 
skriptet i LM som lager categorier. Programmet henter data om categorier fra databasen og bruker det til å lage
widgets. 
Konfigurasjon som trengs er å spesifisere er navnet til nye widgeter og navnet til objekter som skal være i widgeter.
Når den blir kjørt vil den lage widgeter for alle rom. 

Forklaring av virkemåte:
Programmet henter ut alle objekter som inneholder navnet til rom og navnet til et av objektene som ble spesifisert. 
Deretter henter han ut alle categorier og ser etter de som inneholder navnet til rom. Hvis det finnes en slik
category, så lager han en widget for den. 

Objekter må ha navnet til rommet og navnet til objektet som skal være i widgeten.
Samtidig må categori inneholde navnet til rommet.

### Info Widgets 

Denne modulen lager widgets som viser informasjon om et rom. 

Konfigurasjon:
* Navnet til nye widgeter i filene i LM 
* Navnet til rommet som skal vises i widgeten 
* Navnet til objekter som skal vises i widgeten
* Importere en schematikk som inneholder informasjon om hvordan widgeten skal se ut. Denne schematikken må være i .tar 
format. Objekter må være tilknyttet til riktige objekter for det rommet. Titelen (navnet til widgeten) må hete "room"
eller "rom". Denne teksten blir byttet ut med navnet til rommet som widgeten viser.


### Framework & Level 

Denne modulen lager en framework og level for en etasje. 

Før generering:
* Lag en framework i LM som inneholder alle rommene som skal være i etasjen. For hver rom må det være en boks og navnet
til rommet må være på boksen.
* Lag ferdig et rom, det vil si at alle objekter som skal være i rommet må være plassert på boksen. Gjør det for alle 
box typer, for eksempel hvis noen rom i etasjen har en annen boks, plassering eller objekter på boksen. Slike rom 
skal bli brukt som maler for andre rom. 
* Lag virtuele objekter som skal være tilknyttet til boksene. De skal hete "A2002 Farge boks", det skal være en for
hver boks. De skal være tilknyttet til boksene. 

Forklaring:
* kolonnen "Box Types" brukes til å legge til boks typer og slette boks typer. Som standard kommer det en boks type som
heter "default". Til å legge flere double klikk på rådet under den siste og skriv inn navnet til boks typen, da vil 
den bli lagt til og en ny tab med samme navn vil bli lagt til. For å slette en boks type, double klikk på navnet til
boks typen, slett navnet og trykk enter. Da vil boks typen bli slettet.

Alt annet enn kolonnen "Box Types" og importering av schematikker er tilhørende til en boks type.

* Kolonnen "Object names" inneholder navnene til objekter som skal være i rommet. Var klar over at alle objekter som 
er i denne kolonnen må også være tilknyttet til objekter som ligger på boksen. 
* Kolonnen "Slected Rooms" inneholder rommene som skal bruke denne boks typen. For å legge til et rom bruk knappen
ctrl og klikk på alle rommene som skal bruke denne boks typen og trykk enter. Det kan også brukes shift + klikk for
å velge flere rom. Når du trykker enter vil rommene bli lagt til i kolonnen og hvis noen rom allerede er valgt vil de
bli fjernet. Det skal være bare ett rom for hver boks type.
* Velg en boks type som skal brukes som mal for rommene.
* Velg hvilken ikon er brukt som boks 
* Velg hvilken ikon er brukt for trender 
* importer level og framework fra LM til programmet.

Konfigurasjon:
* Som standard bruke









