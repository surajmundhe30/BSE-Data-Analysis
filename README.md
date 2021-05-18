# BSE Data Analysis

## Installation and setup

- Clone this repository with command: `git clone https://github.com/surajmundhe30/BSE-Data-Analysis.git`
- install below all python modules: 
`Django==3.1.2
    redis==3.5.3
    django-redis==4.12.1
    requests
    schedule
    pandas
    `
 - Run the project with `python3 manage.py runserver`



## This application perform below tasks:

- Downloads the equity bhavcopy zip from the above page every day at 18:00 IST for the current date.
- Extracts and parses the CSV file in it.
- Writes the records into Redis with appropriate data structures (Fields: code, name, open, high, low, close).
- Renders a simple VueJS frontend with a search box that allows the stored entries to be searched by name and renders a table of results and optionally downloads the results as CSV. Make this page look nice!
- The search needs to be performed on the backend using Redis.

## This Application looks like below: 
![screenshot](https://user-images.githubusercontent.com/84240273/118405753-d207ac80-b696-11eb-8a95-7f0916d44c8c.PNG)
