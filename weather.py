"""
weather.py

Returns current weather from different cities.
"""

import sys
import urllib.request
import json
import tkinter

#default url
url = "http://api.openweathermap.org/data/2.5/weather" \
        "?q=10001,US" \
        "&units=imperial" \
        "&mode=json" \
        "&APPID=532d313d6a9ec4ea93eb89696983e369"
    
cities = [
    ["10001", "New York City"],
    ["33101", "Miami"],
    ["90001", "Los Angeles"],
    ["60007", "Chicago"],
    ["30301", "Atlanta"],
    ["98101", "Seattle"],
    ["77001", "Houston"]
]

citynames = [city[1] for city in cities]



try:
    infile = urllib.request.urlopen(url)
except urllib.error.URLError as error:
    print(error, file = sys.stderr)
    sys.exit(1)

sequenceOfBytes = infile.read()         #Read the entire input file.
infile.close()

try:
    s = sequenceOfBytes.decode("utf-8") #s is a string.
except UnicodeError as error:
    print(error, file = sys.stderr)
    sys.exit(1)

try:
    bigDictionary = json.loads(s)          #bigDictionary is a dict
except json.JSONDecodeError as error:
    print(error, file = sys.stderr)
    sys.exit(1)

try:
    main = bigDictionary["main"]            #main is a dict
except TypeError:
    print("bigDictionary is not a dictionary", file = sys.stderr)
    sys.exit(1)
except KeyError:
    print("bigDictionary has no key named main", file = sys.stderr)
    sys.exit(1)


#tkinter section:

root = tkinter.Tk()
root.title("Current weather")

#Labels for tkinter:

cityLabel = tkinter.Label(text = "Select which city:", anchor = "e", padx = 5)
cityLabel.grid(row = 0, column = 0, sticky = "e")

tempLabel = tkinter.Label(text = "Temperature:", anchor = "e", padx = 5)
tempLabel.grid(row = 1, column = 0, sticky = "e")

tempResult = tkinter.Label(text = (f'{bigDictionary["main"]["temp"]}° F'), anchor = "w", padx = 5,
                           bg = "white", fg = "blue")
tempResult.grid(row = 1, column = 1, sticky = "ew")

skiesLabel = tkinter.Label(text = "Skies:", anchor = "e", padx = 5)
skiesLabel.grid(row = 2, column = 0, sticky = "e")

skiesResult = tkinter.Label(text = (f'{bigDictionary["weather"][0]["description"]}'), anchor = "w", padx = 5,
                           bg = "white", fg = "blue")
skiesResult.grid(row = 2, column = 1, sticky = "ew")


#default value for drop down menu
drop = tkinter.StringVar(root)
drop.set(cities[0][1])   #default value

def fetchzip(cityname):
    try:
        i = citynames.index(cityname)
    except ValueError as error:
        print(error, file = sys.stderr)
        sys.exit(1)
    zippy = cities[i][0]

    url = f"http://api.openweathermap.org/data/2.5/weather" \
    "?q={},US" \
    "&units=imperial" \
    "&mode=json" \
    "&APPID=532d313d6a9ec4ea93eb89696983e369".format(zippy)

    try:
        infile = urllib.request.urlopen(url)
    except urllib.error.URLError as error:
        print(error, file = sys.stderr)
        sys.exit(1)

    sequenceOfBytes = infile.read()         #Read the entire input file.
    infile.close()

    try:
        s = sequenceOfBytes.decode("utf-8") #s is a string.
    except UnicodeError as error:
        print(error, file = sys.stderr)
        sys.exit(1)

    try:
        bigDictionary = json.loads(s)          #bigDictionary is a dict
    except json.JSONDecodeError as error:
        print(error, file = sys.stderr)
        sys.exit(1)

    try:
        main = bigDictionary["main"]            #main is a dict
    except TypeError:
        print("bigDictionary is not a dictionary", file = sys.stderr)
        sys.exit(1)
    except KeyError:
        print("bigDictionary has no key named main", file = sys.stderr)
        sys.exit(1)
    
    tempResult["text"] = (f'{bigDictionary["main"]["temp"]}° F')
    skiesResult["text"] = (f'{bigDictionary["weather"][0]["description"]}')

#drop downmenu
menu = tkinter.OptionMenu(root, drop, *citynames, command = fetchzip)
menu.grid(row = 0, column = 1, sticky = "ew")

tkinter.mainloop()
