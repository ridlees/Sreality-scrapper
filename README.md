# Sreality-scrapper

A tool to scrape sreality and collect renting offer data across czechia. It comes with scrapper (main.py), script to generate sqlite database and tool to generate report in csv from the said database.

## Installation

pip install -r requirements.txt

## Usage

The tool is designed for cron usage. 

0. Run once createDatabase.py. 
1. Start by running main.py. On first run (or big changes in Sreality listing) it can run for multiple hours. Currently testing running it 4 times a day (every six hours).
2. As often as you want - run createCSV.py to get data.csv

