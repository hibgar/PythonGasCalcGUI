import PySimpleGUI as sg
from haversine import haversine, Unit
import requests
import urllib.parse

# designing the application
sg.theme('DarkBlue12')	
layout = [
	[sg.Text('Please enter the addresses: ')],
	[sg.Text('Address 1', size =(15, 1)), sg.InputText()],
	[sg.Text('Address 2', size =(15, 1)), sg.InputText()],
  [sg.Text('Car\'s MPG' , size =(15, 1)), sg.InputText()],
  [sg.Text('Current Gas Price' , size =(15, 1)), sg.InputText()],
	[sg.Submit(), sg.Cancel()],
  [sg.Text("", key='-TEXT-')]
]

window = sg.Window('Gas Calculator', layout, finalize=True)
event, values = window.read()

# The input data looks like a simple list when automatic numbered
print(event, values[0], values[1], values[2], values[3])

address1 = values[0]
address2 = values[1]
mpg = float(values[2])
gasPrice = float(values[3])

url1 = "https://nominatim.openstreetmap.org/search/" + urllib.parse.quote(address1) + "?format=json"
url2 = "https://nominatim.openstreetmap.org/search/" + urllib.parse.quote(address2) + "?format=json"

response1 = requests.get(url1).json()
response2 = requests.get(url2).json()
#print(type(response2[0]["lat"]))
#print(response1[0]["lon"])

ll1 = (eval(response1[0]["lat"]), eval(response1[0]["lon"])) # (lat, lon)
ll2 = (eval(response2[0]["lat"]), eval(response2[0]["lon"]))
#print(type(ll2[0])) #eval converts to float

dist = haversine(ll1, ll2, unit=Unit.MILES)
print(dist)

gasneeded = dist / mpg
cost = gasneeded * gasPrice
cost = round(cost, 2)

while True:

  if event == 'Submit':
    result = "The cost of gas used for this trip is: " + str(cost)
    window['-TEXT-'].Update(result)
    window.refresh()
  if event == 'Cancel':
    window.close()