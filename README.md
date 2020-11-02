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