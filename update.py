import json
import requests
import urllib.request
from datetime import datetime, timedelta

room = "3439"
today = datetime.today().strftime("%Y-%m-%dT00:00:00Z")
date = (datetime.today() + timedelta(days=60)).strftime("%Y-%m-%dT00:00:00Z")
url = "https://tahvel.edu.ee/hois_back/timetableevents/timetableByRoom/31?from={}&room={}&thru={}".format(today,room,date)
response = requests.get(url)
#data = response.read().decode('utf8')
writeFile =open('data.txt', 'w')
writeFile.write(response.text)
writeFile.close()
