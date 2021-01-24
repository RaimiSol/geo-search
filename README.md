# GeoSearch

Implementation of a basic geographical based search engine.

AIM: Search for policereports or other texts by geographical phrases.

## Overview

The main components are:

- Frontend
  - Framework: Vue
  - Basic user interface for a search engine
- Backend
  - Framework: Flask
  - Simple api that responds to requests from frontend and delivers requested data reading from a postgresql database
- Crawler
  - Framework: Scrapy
  - Crawler writes policereports from https://www.berlin.de/polizei/polizeimeldungen/ to json
- Database
  - Postgresql
  - Processed policereports were imported to a postgresql database
- Data Processing
  - Frameworks: Flair, Spacy
  - Named Entity Recognition to extract geographical phrases from texts

## Contribute

The project does the following:

- A crawler programmed with Scrapy (Python framework) automatically loads police reports from the website https://www.berlin.de/polizei/polizeimeldungen/ into a large JSON file.
- The police reports are processed using the natural language processing frameworks "Spacy" and "Flair" to automatically detect geographic phrases.
- An inverse index is built to search police reports for location information.
- The data is written to a Postgresql database.
- The database is used by a Flask (Python framework) backend to provide a search for police reports by specifying locations.
- The backend is ultimately accessed by a web interface implemented with VueJS, in which a search for police reports by specifying locations is enabled and the locations of individual police reports are displayed on a map.

### Attention:

- The project was one of my first and is not written according to best practices.
- It does not contain any documentation or user manual.
- It does not contain any tests.
- There is no manual for setting up the project.
- Overall, the project does not offer ideal conditions to get started, yet in my opinion it is an exciting application that has potential for more.

### Objectives:

- Create instructions for setting up the project.
- Improve the code.
- Write tests.
- Generalize project: Instead of police reports, use arbitrary text.
- Extend functionality.

If you have questions or are interested, please contact me via Discord or rais22@zedat.fu-berlin.de
