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
    #get date and time for today
    today = datetime.today().strftime("%Y-%m-%dT00:00:00Z")
    #current = datetime.now()
    current = pytz.utc.localize(datetime.utcnow())
    #localize timezone

    timezone = pytz.timezone("Europe/Tallinn")
    currentAware = current.astimezone(timezone)
    currentTime = currentAware.strftime("%H:%M:%S")
    #currentTime = "15:20:00"
    currentTime = datetime.strptime( currentTime,"%H:%M:%S")
    print(currentTime)
    #testDate = "2022-03-15T00:00:00Z"
    #url = "https://httpstat.us/200"
    #headers = {'Accept' : '*/*','Host': 'https://tahvel.edu.ee','Connection' :'keep-alive' }
    url = "https://tahvel.edu.ee/hois_back/timetableevents/timetableByRoom/31?from={}&room={}&thru={}".format(today,room,today)
    print(url)
    #response = urlopen(url)
    # with urlopen(url) as response:
    #body = response.read()
    # if response.status_code != 204:
    #     response = requests.get(url)
    response = requests.get(url)
    response.raise_for_status()
    # response = """{"studyPeriods":"Kevadsemester","timetableEvents":[{"id":5965925,"journalId":null,"subjectStudyPeriodId":44488,"nameEt":"Kestlikkusele suunatud disain (TD7150)","nameEn":"Design for Sustainability (TD7150)","date":"2022-03-16T00:00:00Z","timeStart":"12:15","timeEnd":"17:30","hasStarted":false,"teachers":[{"id":7891,"name":"Marta Moorats"},{"id":8887,"name":"Stella Runnel"}],"rooms":[{"id":3439,"roomCode":"306","buildingCode":"D"}],"studentGroups":[{"id":4270,"code":"MDC21"},{"id":4269,"code":"MDR21"}],"subgroups":[{"id":15605,"code":"MA-students"}],"students":[],"addInfo":"Urmas Tartes","singleEvent":false,"publicEvent":true,"timetableId":5818,"showStudyMaterials":false,"capacityType":"MAHT_a","isPersonal":null,"person":null,"isJuhanEvent":false,"isExam":false,"isOngoing":null,"includesEventStudents":false,"changed":"2022-02-18T12:16:54.972Z","canEdit":null,"canDelete":null,"nameRu":"Kestlikkusele suunatud disain (TD7150)"},{"id":5972277,"journalId":null,"subjectStudyPeriodId":44131,"nameEt":"Emotsionaalselt kestlik aksessuaar (DT7195)","nameEn":"Emotionally Durable Accessory (DT7195)","date":"2022-03-16T00:00:00Z","timeStart":"12:15","timeEnd":"17:30","hasStarted":false,"teachers":[{"id":7891,"name":"Marta Moorats"}],"rooms":[{"id":3439,"roomCode":"306","buildingCode":"D"}],"studentGroups":[{"id":4269,"code":"MDR21"}],"subgroups":[{"id":15611,"code":"MA-tudengid"}],"students":[],"addInfo":"Urmas Tartes","singleEvent":false,"publicEvent":true,"timetableId":5818,"showStudyMaterials":false,"capacityType":"MAHT_a","isPersonal":null,"person":null,"isJuhanEvent":false,"isExam":false,"isOngoing":null,"includesEventStudents":false,"changed":"2022-02-18T12:17:15.254Z","canEdit":null,"canDelete":null,"nameRu":"Emotsionaalselt kestlik aksessuaar (DT7195)"},{"id":6684303,"journalId":null,"subjectStudyPeriodId":null,"nameEt":"VKT koosolek","nameEn":null,"date":"2022-03-16T00:00:00Z","timeStart":"10:00","timeEnd":"12:00","hasStarted":true,"teachers":[],"rooms":[{"id":3439,"roomCode":"306","buildingCode":"D"}],"studentGroups":[],"subgroups":[],"students":[],"addInfo":null,"singleEvent":true,"publicEvent":true,"timetableId":null,"showStudyMaterials":false,"capacityType":null,"isPersonal":false,"person":null,"isJuhanEvent":false,"isExam":false,"isOngoing":null,"includesEventStudents":false,"changed":"2022-03-14T12:49:45.724Z","canEdit":null,"canDelete":null,"nameRu":"VKT koosolek"}],"school":{"id":31,"nameEt":"Eesti Kunstiakadeemia","nameEn":"Estonian Academy of Arts","nameRu":"Eesti Kunstiakadeemia"},"isHigher":true,"personalParam":null,"roomId":3439,"roomCode":"306","buildingCode":"D"}"""
    #data = response.json()
    data = json.loads(response)

    dayEvents = data['timetableEvents']
    #print(dayEvents)
    #sort by start time
    dayEvents = sorted(dayEvents, key=lambda item: item['timeStart'])
    #print(dayEvents)

    for items in dayEvents:
        print(items['nameEn'])
        status = items['isOngoing']
        startTime =datetime.strptime( (items['timeStart'] + ":00"),"%H:%M:00")
        endTime = datetime.strptime( (items['timeEnd'] + ":00"),"%H:%M:00")
        print(startTime)
        print(endTime)
        if currentTime<startTime and (startTime-currentTime >= timedelta(minutes=60)):
            availableStatus = "YES🎉"
            subText = "Class is free until {}".format(items['timeStart'])
            #subText = "There is another class in: {}".format(startTime-currentTime)
            backColor = "#8AC05E"
            break
        elif currentTime<startTime:
            availableStatus = "YES,🤔 but.."
            subText = "Class is free until {}".format(items['timeStart'])
            subText = "There is another class in {} minutes".format(int((startTime-currentTime).total_seconds() / 60))
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

    # for items in dayEvents:
    #     print(items['nameEn'])
    #     status = items['isOngoing']
    #     startTime =datetime.strptime( (items['timeStart'] + ":00"),"%H:%M:00")
    #     endTime = datetime.strptime( (items['timeEnd'] + ":00"),"%H:%M:00")
    #     print(startTime)
    #     print(endTime)
    #     if time_in_range(startTime, endTime, currentTime):
    #         availableStatus = "No😔"
    #         subText = "{} will end at {}".format(items['nameEn'],items['timeEnd'])
    #         backColor = "#F04A32"
    #         print("status No")
    #     else:
    #         availableStatus = "YES🎉"
    #         backColor = "#8AC05E"
    #         if currentTime<=startTime:
    #             subText = "Class is free until {}".format(items['timeStart'])
    #         else:
    #             subText = "Class is free until tomorrow!"
    #
    #         print("status Yes")


    #Center text
        # Render HTML with count variable
        #print(status)
    print(time_in_range(startTime, endTime, currentTime))

    return render_template("index.html", status=availableStatus, backColor=backColor, subText=subText)

    #st.markdown("<h1 style='text-align: center; color: white;'>{}</h1>".format(status), unsafe_allow_html=True)
if __name__ == "__main__":
    #app.run(host='localhost', port=5000, debug=True)
    #from waitress import serve
    #serve(app,host="0.0.0.0")
    app.run(host="0.0.0.0")
