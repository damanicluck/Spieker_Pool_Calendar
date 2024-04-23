import requests
import re
import csv
from bs4 import BeautifulSoup

import chromedriver_autoinstaller
from selenium import webdriver

chromedriver_autoinstaller.install()

daysWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

fields = ["Subject", "Start date", "Start time", "End Date", "End time", "All Day Event", "Location"]
fileName = "times.csv"
url = "https://recwell.berkeley.edu/schedules-reservations/lap-swim/"
urlTest = "https://www.geeksforgeeks.org/data-structures/" 
poolName = "Spieker"
validDivs = []
# returns True if successful, false if failure for writing to csv
def csvConvert(fileName, getDivs, mode):
    # create csv writer object, write the fields, write the data rows
    # If quoting is set to csv.QUOTE_MINIMAL, then .writerow() will quote fields only if they contain the delimiter or the quotechar. This is the default case.
    # csv file format for gcal:
    with open(fileName, mode) as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',  quotechar='"', quoting=csv.QUOTE_MINIMAL)
        parsedDivs = parsing(getDivs)
        for div in parsedDivs:
            csvwriter.writerow(div)
    return True

def findExpression(word, sequence):
    for seq in sequence:
        if word == seq:
            return True
    return False

driver = webdriver.Chrome()
driver.get(url)
response = driver.page_source
soup = BeautifulSoup(response, 'html.parser')
div = soup.find_all("div", {"class": "lw_events_day"})
for row in div:
    splitDiv = row.text.strip().split()
    containsName = findExpression(poolName, splitDiv)
    # If the row is a row for the poolname make gcal invites for those.
    if containsName:
        validDivs.append(row)

if csvConvert(fileName, validDivs, 'a'):
    print("Successful csv reading and writing")