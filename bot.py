import mechanize
import http
import time
import sys
from bs4 import BeautifulSoup
from os import path

browser = mechanize.Browser()
cookieJar = http.cookiejar.CookieJar()
browser.set_cookiejar(cookieJar)

browser.set_handle_robots(False)   # ignore robots
browser.set_handle_refresh(False)  # can sometimes hang without this

browser.addheaders = [('User-agent', 'Firefox')]
argument = sys.argv
city = str(argument[1])
url = "https://m.rosszlanyok.hu/videkilanyok/varos-"+ city +"-lanyok"

print(url)

page = browser.open(url)

html = page.read()
html = BeautifulSoup(html, 'html.parser')
girlNames = html.findAll('p',{"class":"name"})

# Beolvasom az előző futás eredményét
isFileExist = path.exists("girls.txt")
oldGirls = []
if isFileExist:
    try:
        file = open("girls.txt", "r")
        lines = file.readlines()
        for index, line in enumerate(lines):
            oldGirls.append(line.strip())
    finally:
        file.close()

# Elmentem a jelenlegi lányok nevét
try:
    file = open("girls.txt", "w")
    for name in girlNames:
        file.write(name.get_text().strip()+"\n")
finally:
    file.close()

# Beolvasom az új mentés eredményét
newGirls = []
try:
    file = open("girls.txt", "r")
    lines = file.readlines()
    for index, line in enumerate(lines):
        newGirls.append(line.strip())
finally:
    file.close()

# Megvizsgálom kik az új lányok és kik mentek el, ehhez megvizsgálom az új lányok neve
# szerepel-e a régi lányok között ha igen akkor maradtak ha nem akkor újak
# Megvisgálom azt is hogy a régi lányok neve az szerepel-e az újak között, ha nem akkor lementek
goneGirls = []
for oldGirl in oldGirls:
    if not oldGirl in newGirls:
        goneGirls.append(oldGirl)

freshGirls = []
for newGirl in newGirls:
    if not newGirl in oldGirls:
        freshGirls.append(newGirl)

print("Elmentek:\n")
print(goneGirls)

print("\n")

print("Újak vagy maradtak:\n")
print(freshGirls)



