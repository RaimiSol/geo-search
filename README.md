# GeoSearch
Implementation of a basic geographical based search engine.

AIM: Search for policereports or other texts by geographical phrases.

## Overview

The main components are:

* Frontend
  * Framework: Vue
  * Basic user interface for a search engine
* Backend
  * Framework: Flask
  * Simple api that responds to requests from frontend and delivers requested data reading from a postgresql database
* Crawler
  * Framework: Scrapy
  * Crawler writes policereports from https://www.berlin.de/polizei/polizeimeldungen/ to json
* Database
  * Postgresql
  * Processed policereports were imported to a postgresql database
* Data Processing
  * Frameworks: Flair, Spacy
  * Named Entity Recognition to extract geographical phrases from texts
  
## Mitmachen

Das Projekt macht Folgendes:
- Ein mit Scrapy (Python-Framework) programmierter Crawler lädt automatisch Polizeiberichte von der Webseite https://www.berlin.de/polizei/polizeimeldungen/ in eine große JSON-Datei.
- Die Polizeiberichte werden mit den NaturalLanguageProcessing-Frameworks "Spacy" und "Flair" verarbeitet, um automatisch geografische Phrasen zu erkennen.
- Es wird ein inverser Index aufgebaut, um Polizeiberichte nach Ortsangaben suchen zu können.
- Die Daten werden in eine Postgresql Datenbank geschrieben.
- Die Datenbank wird von einem Flask (Python-Framework) Backend verwendet um eine Suche nach Polizeiberichten durch Angabe von Orten bereitzustellen.
- Das Backend wird letztendlich von einer mit VueJS implementierten Weboberfläche angesprochen, in welchem eine Suche nach Polizeiberichten durch Angabe von Orten ermöglicht wird und die Orte einzelner Polizeiberichte werden auf einer Karte dargestellt.

Achtung:
- Das Projekt ist eines meiner ersten gewesen und ist nicht nach BestPractices geschrieben.
- Es enthält keine Dokumentation und kein Benutzerhandbuch.
- Es enthält keine Tests.
- Es sind bis auf das Frontend nur einzelne Python Skripte.
- Zum Aufsetzen des Projekts fehlt noch eine Anleitung.

Insgesamt bietet das Projekt keine idealen Bedingungen zum Einsteigen, dennoch ist es meiner Meinung nach eine spannende Anwendung die noch Potential für mehr hat.

Ziele:
- Anleitung zum Aufsetzen des Projekts erstellen.
- Code aufbessern.
- Tests schreiben.
- Projekt generalisieren: Statt Polizeiberichte, beliebige Texte verwenden.
- Funktionalität erweitern.

Bei Fragen oder Interesse meldet euch gerne bei mir über Discord oder rais22@zedat.fu-berlin.de
