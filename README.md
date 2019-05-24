# FU enrollments

## Setup

### Configure Python environment

TODO

### Install Tabula

`wget https://github.com/tabulapdf/tabula-java/releases/download/v1.0.2/tabula-1.0.2-jar-with-dependencies.jar`

## Steps

## 1. Scrape list of `.pdf`s from website

`python scripts/scrape_pdf_list.py`

## 2. Download `.pdf`s

`python scripts/download_pdfs.py`

## 3. Extract data from `.pdf`s to `.csv` using Tabula

# Data ideas

match subject with Fachbereich

[Studienangebot](https://www.fu-berlin.de/studium/studienangebot/grundstaendige/index.html)

# Visualization ideas

- gender by subject (bachelor/master)
  - show only entries with over n people
  - show development over time
  - filters
    - degree (bachelor/master)
- geographic heatmap for how many people are from
  - which Bundesland in Germany
  - which country
- visualization of study duration (bachelor/master)
  - show mean study duration
  - for every semester show
    - % continue
    - % dropout
    - % graduate
  - filters
    - degree (bachelor/master)
    - subject
