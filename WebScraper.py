import bs4
import requests
from selenium import webdriver
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date
# Grab only neccessary functions
#from urllib.request import urlopen as getURL #uReq
from bs4 import BeautifulSoup as bSoup #soup

scope =["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("sheetscreds.json", scope)
client = gspread.authorize(creds)


fantURL = 'https://fantasy.espn.com/hockey/league/standings?leagueId=39095&seasonId=2021'


# Stores page info

driver = webdriver.Chrome()

driver.get(fantURL)
time.sleep(5)
content = driver.page_source.encode('utf-8').strip()
fantSoup = bSoup(content, "html.parser")

# Grabs each name

tableNames = fantSoup.find_all('div', {'class':'jsx-2810852873 table--cell team__column'})
names = []
for teams in tableNames:
    spans = teams.find_all('span', {'class': 'teamName truncate'})
    for span in spans:
        names.append(span.attrs['title'])
    
tablePoints = fantSoup.find_all('div', {'class':'jsx-2810852873 table--cell points tar'})
points = []
for teams in tablePoints:
    points.append(teams.text)

driver.quit()

teamDict ={}
for i in range(len(points)):
    teamDict[names[i]] = float(points[i])

print(teamDict)

sheet = client.open("Moves Like Jagr Points Race").sheet1

today = date.today()

insertRow = [today.strftime("%d/%m/%Y"), teamDict['Team A'], teamDict['Team B'], teamDict['Team C '], teamDict['Team D'], teamDict['Team E'], teamDict['Team F']]

sheet.insert_row(insertRow, 2)
