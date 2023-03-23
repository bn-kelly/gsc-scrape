# gsc-scrape

## Overview
This script is to download external link Urls from Google search console.

## Requirement
Python 3.7+

## Download
```
$ git clone https://github.com/bn-kelly/gsc-scrape.git
```

## Environment Setup
```commandline
$ cd gsc-scrape
$ python3 -m venv venv
$ source ./venv/bin/activate
$ pip install -r requirements.txt
```

## Run
```commandline
python script.py

site url: https://www.example.com/  (Make sure you have the website in Google Search Console)
firefox binary path: /snap/firefox/1635/usr/lib/firefox/firefox (Firefox binary path)
firefox profile path: /home/measurable/snap/firefox/common/.mozilla/firefox/26i5plou.default (Firefox profile path)
output file: output.csv (Output file name)
```
The message `finished` will be shown when the script finished the scraping
