"""
weather.py

Display the current weather (including icon) in different cities.
"""

import sys
import urllib.parse
import urllib.request
import json
import tkinter

zipcodes = {
    "Atlanta":       "30301",
    "Boston":        "02109",
    "Chicago":       "60007",
    "Denver":        "80202",
    "Houston":       "77001",
    "Los Angeles":   "90001",
    "Miami":         "33101",
    "New York":      "10004",
    "San Francisco": "94102",
    "Seattle":       "98101"
}

defaultCity = "New York"
citynames = zipcodes.keys()
maxLen = len(max(citynames, key = len))   #length of longest name

#data is a tuple containing 5 smaller tuples.
#The second half of the last 4 of them is a function.

data = (
    ("Select your city", None),
    ("Temperature",      lambda d: f'{int(d["main"]["temp"])}° F'),
    ("Wind speed",       lambda d: f'{int(d["wind"]["speed"])} mph'),
    ("Humidity",         lambda d: f'{d["main"]["humidity"]}%'),
    ("Skies",            lambda d: f'{d["weather"][0]["description"]}')
)

backgroundColor = {      #of the tkinter.Label that displays the icon
    "d": "sky blue",     #day
    "n": "midnight blue" #night
}

#This function is called when the program is launched,
#and when the user selects a city.

def command(cityname):
    query = {                               #query is a dictionary
        "q":     f"{zipcodes[cityname]},US",
        "units": "imperial",
        "mode":  "json",
        "APPID": "532d313d6a9ec4ea93eb89696983e369"
    }

    params = urllib.parse.urlencode(query)  #params is a string
    url = f"http://api.openweathermap.org/data/2.5/weather?{params}"

    try:
        infile = urllib.request.urlopen(url)
    except urllib.error.URLError as error:
        print(error, url, file = sys.stderr)
        sys.exit(1)

    sequenceOfBytes = infile.read()         #Read the entire input file.
    infile.close()

    try:
        s = sequenceOfBytes.decode("utf-8") #s is a string.
    except UnicodeError as error:
        print(error, file = sys.stderr)
        sys.exit(1)

    try:
        bigDict = json.loads(s)
    except json.JSONDecodeError as error:
        print(error, file = sys.stderr)
        sys.exit(1)

    assert isinstance(bigDict, dict)

    for label, datum in zip(labels, data[1:]):
        label["text"] = datum[1](bigDict)

    weather = bigDict["weather"][0] #bigDict["weather"] is a list.
    icon = weather["icon"]          #first characters of name of icon file
    url = f'http://openweathermap.org/img/wn/{icon}@2x.png'

    try:
        infile = urllib.request.urlopen(url)
    except urllib.error.URLError as error:
        print(error, file = sys.stderr)
        sys.exit(1)

    sequenceOfBytes = infile.read()
    infile.close()

    try:
        image = tkinter.PhotoImage(data = sequenceOfBytes)
    except tkinter.TclError as error:
        print(error, file = sys.stderr)
        sys.exit(1)

    try:
        bg = backgroundColor[icon[-1]]
    except KeyError:
        iconLabel.configure(image = image)
    else:
        iconLabel.configure(image = image, bg = bg)

    iconLabel.image = image   #Strange that you need this too.

#Create the tkinter interface when the program is launched.

root = tkinter.Tk()
root.title("Current weather")
padx = 5

#dropdown menu
dropVariable = tkinter.StringVar(root)
dropVariable.set(defaultCity)
menu = tkinter.OptionMenu(root, dropVariable, *citynames, command = command)
menu.config(width = maxLen)
menu.grid(row = 0, column = 1, sticky = "ew")

#Create the labels that are captions.

for row, datum in enumerate(data):
    label = tkinter.Label(text = f"{datum[0]}:", anchor = "e", padx = padx)
    label.grid(row = row, column = 0, sticky = "ew")

#Create the labels that display information.
labels = []

for row in range(1, len(data)):
    label = tkinter.Label(anchor = "w", padx = padx, fg = "blue")
    label.grid(row = row, column = 1, sticky = "ew")
    labels.append(label)

iconLabel = tkinter.Label(root)
iconLabel.grid(row = len(data), column = 0, columnspan = 2, sticky = "ew")

command(defaultCity)   #Begin by displaying the data for the default city.
tkinter.mainloop()
