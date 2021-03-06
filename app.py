from urllib.request import urlopen
from datetime import datetime, timedelta
import pytz
from flask import Flask, render_template
import json
import requests
def time_in_range(start, end, current):
    """Returns whether current is in the range [start, end]"""
    return start <= current <= end

app = Flask(__name__)
@app.route("/")
def index():
    #room id
    room = "3439"
    availableStatus = "YES🎉"
    backColor = "#8AC05E"
    subText = "No data found for today"
    #get date and time for today
    today = datetime.today().strftime("%Y-%m-%dT00:00:00Z")
    #today = "2022-03-17T00:00:00Z"
    #current = datetime.now()
    current = pytz.utc.localize(datetime.utcnow())

    #localize timezone
    timezone = pytz.timezone("Europe/Tallinn")
    currentAware = current.astimezone(timezone)
    currentTime = currentAware.strftime("%H:%M:%S")
    #currentTime = "22:00:00"
    currentTime = datetime.strptime( currentTime,"%H:%M:%S")
    print(currentTime)
    url = "https://tahvel.edu.ee/hois_back/timetableevents/timetableByRoom/31?from={}&room={}&thru={}".format(today,room,today)
    print(url)
    #response = urlopen(url)
    # with urlopen(url) as response:
    #body = response.read()
    # if response.status_code != 204:
    #response = requests.get(url)
    #response = requests.get(url)
    #response.raise_for_status()

    # data = response.json()

    file = open('data.txt','r',encoding="latin")


    data = json.load(file)

    dayEvents = data['timetableEvents']
    #print(dayEvents)
    #sort by start time
    dayEvents = sorted(dayEvents, key=lambda item: item['timeStart'])
    #print(dayEvents)
    print('today is {}'.format(today))
    for items in dayEvents:
        if datetime.strptime((items['date'].split('T'))[0],"%Y-%m-%d")==datetime.strptime((today.split('T'))[0],"%Y-%m-%d"):
            print(items['nameEn'])
            status = items['isOngoing']
            startTime =datetime.strptime( (items['timeStart'] + ":00"),"%H:%M:00")
            endTime = datetime.strptime( (items['timeEnd'] + ":00"),"%H:%M:00")
            print(datetime.strptime((items['date'].split('T'))[0],"%Y-%m-%d"))
            print(startTime)
            print(endTime)
            if currentTime<startTime and (startTime-currentTime >= timedelta(minutes=60)):
                availableStatus = "YES🎉"
                subText = """Class is free until {}""".format(items['timeStart'])
                backColor = "#8AC05E"
                break
            elif currentTime<startTime:
                availableStatus = "Yes, but.."
                subText = "{} will start in {} minutes".format(items['nameEn'],int((startTime-currentTime).total_seconds() / 60))
                backColor = "#FEBB23"
                break
            elif time_in_range(startTime, endTime, currentTime):
                availableStatus = "No😔"
                subText = "{} will end at {}".format(items['nameEn'],items['timeEnd'])
                backColor = "#F04A32"
                print("status No")
                break
            else:
                availableStatus = "YES🎉"
                backColor = "#8AC05E"
                subText = "Class is free until tomorrow!"




    #Center text
        # Render HTML with count variable
        #print(status)
    #print(time_in_range(startTime, endTime, currentTime))

    return render_template("index.html", status=availableStatus, backColor=backColor, subText=subText)

    #st.markdown("<h1 style='text-align: center; color: white;'>{}</h1>".format(status), unsafe_allow_html=True)
if __name__ == "__main__":
    #app.run(host='localhost', port=5000, debug=True)
    #from waitress import serve
    #serve(app,host="0.0.0.0")
    app.run(host="0.0.0.0")
