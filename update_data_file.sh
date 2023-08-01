#!/usr/bin/env bash
# By: Melroy van den Berg
# Description: Retrieve the latest user-agent strings using the web scraper and save it within the data folder

# Go to the Useragent scraper folder
cd cache_scraper

# Prepare virtual environment
python -m virtualenv env

# Activate virtual env
source env/bin/activate

# Install Python deps
pip3 install -r ./requirements.txt

# Run spider (output file should end in: website/cache.json)
./start_spider.py

# Copy to data file of fake_useragent Python project
cp website/cache.json ../src/fake_useragent/data/browsers.json
