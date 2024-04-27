import csv
from bs4 import BeautifulSoup
import datetime

import chromedriver_autoinstaller
from selenium import webdriver

chromedriver_autoinstaller.install()

daysWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
fields = ["Subject", "Start date", "Start time", "End Date", "End time", "All Day Event", "Location"]
fileName = "times.csv"
url = "https://recwell.berkeley.edu/schedules-reservations/lap-swim/"
urlTest = "https://www.geeksforgeeks.org/data-structures/" 
poolName = "Spieker"
eventName = "Lap Swim"
AllDayEvent = "FALSE"
location = "Spieker RSF Pool"

# returns True if successful, false if failure for writing to csv
def csvConvert(fileName, getDivs, mode):
    # create csv writer object, write the fields, write the data rows
    # If quoting is set to csv.QUOTE_MINIMAL, then .writerow() will quote fields only if they contain the delimiter or the quotechar. This is the default case.
    # csv file format for gcal:
    with open(fileName, mode) as csvfile:
        csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_NONE, delimiter='|', quotechar='',escapechar='\\')
        parsedDivs = parsing(getDivs)
        for div in parsedDivs:
            csvwriter.writerow(div)

def findExpression(word, sequence):
    for seq in sequence:
        if word == seq:
            return True
    return False

def parsing(divs):
    # after some experimentation we see that duplicate entries dont result in duplicate events in gcal
    storedDivs = []
    for div in divs:
        split = div.text.strip().split()
        month = months.index(split[1])+1
        day = split[2]
        year = datetime.datetime.now().year
        constructDate = [str(month), str(day), str(year)]
        startDate = "/".join(constructDate)
        poolIndexes = [i for i in range(len(split)) if split[i] == poolName and split[i+1] != '-']
        for i in poolIndexes:
            hyphenIndex = i - 3
            amPM = "PM" if split[i-1] == 'p.m.' else "AM"
            temp1 = split[hyphenIndex + 1]
            num = temp1 if len(temp1) > 1 else temp1+":00"
            endTime = num + " " + amPM
            #parsing startTime
            continuousTime = False if split[hyphenIndex - 1] == 'p.m.' or split[hyphenIndex - 1] == 'a.m.' else True
            if continuousTime:
                firstNum= split[hyphenIndex - 1]
                parsedFirstNum = firstNum if len(temp1) > 2 else firstNum + ":00"
                startTime = parsedFirstNum + " " + amPM
            else:
                firstNum = split[hyphenIndex - 2]
                parsedFirstNum = firstNum if len(firstNum) > 2 else firstNum + ":00"
                ending = "PM" if split[hyphenIndex-1] == 'p.m.' else "AM"
                startTime = parsedFirstNum + " " + ending
            constructRow = [eventName, startDate, startTime, startDate, endTime, AllDayEvent, location]
            storedDivs.append([', '.join(constructRow)])
    return storedDivs
driver = webdriver.Chrome()
driver.get(url)
response = driver.page_source
soup = BeautifulSoup(response, 'html.parser')
div = soup.find_all("div", class_ = "lw_events_day")
for row in div:
    splitDiv = row.text.strip().split()
    containsName = findExpression(poolName, splitDiv)
    # If the row is a row for the poolname make gcal invites for those.
    if not containsName:
        div.remove(row)
csvConvert(fileName, div, 'a')
print("Successful csv reading and writing")