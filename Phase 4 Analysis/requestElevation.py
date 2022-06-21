#THIS PROGRAM MUST BE RUN FIRST!!!!!!!!

import requests
import json
import csv

response = requests.get('https://api.open-elevation.com/api/v1/lookup?locations=27.9881,86.9250|36.72586,73.17313|31.5, 35.5') 

data = response.json() 

CSV = open("elevations.csv", "w", newline="")
CSV.close()


with open("elevations.csv", "a", newline="") as CSV:
  writer = csv.writer(CSV)
  header = ("LoopNum", "LatLong1","latLong2", "Lat1", "Long1" , "Elevation" )
  writer.writerow(header)
CSV.close()


#Gets Lat_1 data from datafile 1 and adds it to Lat_1 list
latOne = []
longOne = []
latLongOne = []
latLongTwo = []
loopNumbers = []
with open('datafile1.csv','r') as CSV1:
  plots = csv.reader(CSV1, delimiter=',')
  for row in plots:
  	if (row[0] == 'LoopNumber'):
  		print("Skipped")
  		pass
  	else:
  		loopNum = row[0]
  		lat1 = row[3]
  		long1 = row[4]
  		lat2 = row[5]
  		long2 = row[6]
  		loopNumbers.append(loopNum)
  		latOne.append(lat1)
  		longOne.append(long1)
  		latLongOne.append(str(lat1)+ "," + str(long1))
  		latLongTwo.append(str(lat2) + "," + str(long2))
  		#response = requests.get(f'https://api.open-elevation.com/api/v1/lookup?locations={latLongOne}|{latLongTwo}')
  		#data = response.json() 
  		#print(data)
print(latLongOne)
print(latLongTwo)
 
elevation = []
for i in range(0, len(loopNumbers) - 3, 3):
	print(i)
	try:
		response = requests.get(f'https://api.open-elevation.com/api/v1/lookup?locations={latLongOne[i]}|{latLongOne[i+1]}|{latLongOne[i+2]}')
	except:
		pass
	data = response.json()

	for r in range(0, 3):
		elevationData = data['results'][r]['elevation']
		elevation.append(elevationData)
		print(elevationData)

with open("elevations.csv", "a", newline = "") as CSV:
	writer = csv.writer(CSV)
	for i in range(0, len(loopNumbers) - 3):
		row = (loopNumbers[i], latLongOne[i], latLongTwo[i], latOne[i], longOne[i], elevation[i])
		writer.writerow(row)
		print("Succsesfully wrote to datafile")
	CSV.close()



"""
    if str(row[3]) != "Latitude1":
      lat1 = baseData.append(float(row[3]))
    if str(row[4]) != "Longtitude1":
      long1 = baseData.append(float(row[4]))
    if str(row[5]) != "Latitude2":
      lat2 = baseData.append(float(row[5]))
    if str(row[6]) != "Longtitude2":
      long2 = baseData.append(float(row[6]))
    latLongOne = (lat1+ "," + long1)
    print(latLongOne)  
"""

one = (data['results'][0])
two = (data['results'][1])
three = (data['results'][2])
elevation = data['results'][1]['elevation']


type(data)
print(one)
print(two)
print(elevation)
