import requests
import re
from bs4 import BeautifulSoup
from PlayerCountRow import PlayerCountRow
from typing import List
from datetime import datetime
import sys
import os
import csv

def getTotalPlayerCount(totalPCElement) -> PlayerCountRow:
    totalPC = re.search("There are currently (.*) people playing!", totalPCElement.text)
    return PlayerCountRow("TOTAL", "TOTAL", totalPC.group(1).replace(",", ""), "TOTAL", "TOTAL", "TOTAL", datetime.now())


def getWorldPlayerCount(worldRow) -> PlayerCountRow:
    cells = worldRow.find_all("td")

    # Get World via url href
    worldUrl = cells[0].find("a", class_="server-list__world-link")["href"]
    world = worldUrl.split("?world=",1)[1]

    return PlayerCountRow(world, cells[0].text.strip(), cells[1].text.split(" ")[0], cells[2].text , cells[3].text , cells[4].text, datetime.now())

    

def getAllWorldsPlayerCount(worldRows) -> List[PlayerCountRow]:
    worldCounts : List[PlayerCountRow] = []

    for worldRow in worldRows:
        worldCounts.append(getWorldPlayerCount(worldRow))

    return worldCounts



# Get run arguments, remove first one (as it indicates what file to run, not interested)
# Make file location configurable via run args
args = sys.argv
args.pop(0)
print(f'Run arguments {args}')

file_location = '.\data'

if len(args) == 0:
    print(f'No file location provided')
elif len(args) > 1:
    print(f'Too many arguments')
else: 
    file_location = args.pop()
    
file_location = os.path.join(file_location, '')
print(f'File location set to {file_location}')


# The page that we are going to scrape
worldUrl : str = 'https://oldschool.runescape.com/a=97/slu?order=WMLPA'


# Scrape page, and put in parser (BeautifulSoup)
page = requests.get(worldUrl)
soup = BeautifulSoup(page.content, "html.parser")


# Get Total + World rows
totalPlayerCount = getTotalPlayerCount(soup.find("p", class_="player-count"))
worldsPlayerCount = getAllWorldsPlayerCount(soup.find_all("tr", class_="server-list__row"))
worldsPlayerCount.append(totalPlayerCount)


# Set up for writing to csv file
file_headers = ['world', 'oldSchoolWorld', 'count', 'location', 'type', 'activity', 'datetime']
file_name = f'OSRSWorldPlayerCount_{datetime.now().strftime("%Y%m%d")}.csv'
file_path = file_location + file_name
file_exists = os.path.isfile(file_path)

# Write to csv file
with open (file_path, 'a+', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')

    # First time, write header row
    if not file_exists:
        writer.writerow(file_headers)

    # Write the rows to csv
    writer.writerows(worldsPlayerCount)
    print(f'Wrote {len(worldsPlayerCount)} lines to file {file_path}')
