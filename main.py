import requests
# import time
import csv
from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.support.ui import WebDriverWait

daysWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
url = "https://recwell.berkeley.edu/schedules-reservations/lap-swim/"
url_test = "https://www.geeksforgeeks.org/data-structures/" 
filename = "times.csv"
fields = ["Subject", "Start data", "Start time", "End time"]
my_data = []

# returns response if successful, false if failure
def getResponse(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.exceptions.HTTPError as errh:
        print(f"Http Error: {errh}")
        return False
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
        return False
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
        return False
    except requests.exceptions.RequestException as err:
        print(f"OOps: Something Else: {err}")
        return False
    return response

# returns a n by 4 array
def getDivs():
    return None

# returns True if successful, false if failure for writing to csv
def csvConvert():
    # create csv writer object, write the fields, write the data rows
    # csv file format for gcal:
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(getDivs)
        return True

def errorCheck(type, message):
    if message is False: 
        print(type + "failure")

def main():
    response = getResponse(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    div_text = soup.find(id = "main")
    # print(div_text)
    print(div_text.get_text())
main()