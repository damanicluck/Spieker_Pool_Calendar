import requests
import csv
from bs4 import BeautifulSoup

import chromedriver_autoinstaller
from selenium import webdriver
from bs4 import BeautifulSoup

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
    class_list = set()
    response = getResponse(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    div = soup.find_all("div")

    # tags = {tag.name for tag in soup.find_all()} 
    # for tag in tags: 
  
    #     # find all element of tag 
    #     for i in soup.find_all( tag ): 
    
    #         # if tag has attribute of class 
    #         if i.has_attr( "class" ): 
    
    #             if len( i['class'] ) != 0: 
    #                 class_list.add(" ".join( i['class'])) 
  
    # print(class_list)     

    # print(soup.prettify())
    # print(div)
    # print(div)
    for i in div:
        print(i)
main()