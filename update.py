import json
import requests
import urllib.request
from datetime import datetime, timedelta

room = "3439"
today = datetime.today().strftime("%Y-%m-%dT00:00:00Z")
date = (datetime.today() + timedelta(days=60)).strftime("%Y-%m-%dT00:00:00Z")
url = "https://tahvel.edu.ee/hois_back/timetableevents/timetableByRoom/31?from={}&room={}&thru={}".format(today,room,date)
response = urllib.request.urlopen(url)
data = response.read().decode('UTF-8')
writeFile =open('data.json', 'w')
writeFile.write(data)
writeFile.close()
