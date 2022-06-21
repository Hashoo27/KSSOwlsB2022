#THIS FILE MUST BE RUN SECOND!! AFTER "GetElevation.py"


import csv
from pathlib import Path
from math import cos, asin, sqrt, pi
import matplotlib.pyplot as plt
import numpy as np



CSV = open("estimatedHeights.csv", "w")
CSV.close()



with open("nightDay.csv", "w", newline ="") as CSV:
  writer = csv.writer(CSV)
  header = ("NightDay", "Velocity")
  writer.writerow(header)
CSV.close()

with open("estimatedHeights.csv", "w", newline ="") as CSV:
  writer = csv.writer(CSV)
  header = ("elevations", "Lat1", "Long1")
  writer.writerow(header)
CSV.close()

with open("standardizedElevation.csv", "w", newline = "") as CSV:
  writer = csv.writer(CSV)
  header = ( "Elevation", "Lat1", "Long1")
  writer.writerow(header)
CSV.close()

#Gets KM/s data from datafile 1 and adds it to baseData list
baseData = []
with open('datafile1.csv','r') as CSV2:
  plots = csv.reader(CSV2, delimiter=',')
  for row in plots:
    if str(row[8]) != "km/s":
      baseData.append(float(row[8]))


#Gets the image classification data from datafile 2 and converts it into 0, 0.5 or 1 depending on the result.
nightDay = []
with open('datafile4.csv','r') as CSV4:
  plots = csv.reader(CSV4, delimiter=',')

  for row in plots:
  	print(row)
  	print(len(row))
  	if (len(row) != 1):	
  		for i in range(3):
	  		print("Passed")
		  	if (row[1] == "Day"):
		  		nightDay.append(1)
		  	elif (row[1] == "Twilight"):
		  		nightDay.append(2)
		  	elif (row[1] == "Night"):
		  		nightDay.append(3)


#Gets elevation data from datafile and adds it to elevationData list
latOne = []
longOne = []
elevationData = []
with open('elevations.csv','r') as CSV2:
  plots = csv.reader(CSV2, delimiter=',')

  for row in plots:
  	print(row)
  	if (str(row[5]) != "Elevation" and str(row) != ""):
  			elevationData.append(row[5])
  			latOne.append(row[3])
  			longOne.append(row[4])


def standardize(data, endList, minMax):
	minData = float(min(data))

	#Defines the minimum value for the standardization
	minValue = float(min(minMax))

	#Adds the required amount to ALL data values to make all of them posisitve number
	if minData < 0:
		for index in range(len(data)):
			#adds the abosolute value of the lowest value of the data set to each datapoint
			data[index] = float(data[index]) + abs(minData)


	maxData = float(max(data))
	minData = float(min(data))

	if minValue < 0:
		for index in range(len(minMax)):
			minMax[index] = float(minMax[index]) + abs(minValue)
	
	#Defines the maximum value for standardization
	minValue = float(min(minMax))
	maxValue = float(max(minMax))

	for i in data:
		i = float(i)
		#Standerdizes the data range to the smallest number and largest number in the specified MinMax parameter
		oneToZero = ((maxValue-minValue)*(i - minData)/(maxData-minData)) + minValue
		#Changes the oneToZero value into a value between -1 and 1
		#oneToOne = (oneToZero-0.5)*2
		endList.append(oneToZero)


standardizedData = []
standardize( baseData, standardizedData, elevationData)

standardizedElevations = []
standardize(elevationData, standardizedElevations, elevationData)


#Compares each value against the average of its neighbours, and if it is above a certain threshold, it adds it to the list. 
rises = []
broad = []
for num in range(0, len(standardizedData)-4):
	check = (standardizedData[num] - ( (standardizedData[num-1] + standardizedData[num+1])/2))
	if ( check > 0.05 or check < -0.05):
		rises.append(check);
	else:
		rises.append(0)
	broad.append(check)

fourAvg = []
for num in range(0, len(standardizedData)-4):
	check = (standardizedData[num] - ( (standardizedData[num-1] + standardizedData[num-2])+ standardizedData[num+1] + standardizedData[num+2])/4)
	#print(check)
	if ( check > 140 ):
		fourAvg.append(check);
	else:
		fourAvg.append(0)


oneToZeroFourAvg = []
print(fourAvg)
standardize(fourAvg, oneToZeroFourAvg, elevationData)

with open("estimatedHeights.csv", "a", newline = "") as CSV:
	writer = csv.writer(CSV)
	for i in range(0, len(oneToZeroFourAvg)):
		row = (oneToZeroFourAvg[i], latOne[i], longOne[i])
		writer.writerow(row)
		#print("Succsesfully wrote to datafile")
	CSV.close()


with open("standardizedElevation.csv", "a", newline = "") as CSV:
	writer = csv.writer(CSV)
	for i in range(0, len(standardizedElevations)):
		row = (standardizedElevations[i], latOne[i], longOne[i])
		writer.writerow(row)
		#print("Succsesfully wrote to datafile")
	CSV.close()

standardizedbaseDataToNightDay = []
standardize(baseData, standardizedbaseDataToNightDay, nightDay)

print("THE DATA IS HERE BOIS!!")
print(standardizedbaseDataToNightDay)
print("THE DATA IS UP THERE")
with open("nightDay.csv", "a", newline = "") as CSV:
	writer = csv.writer(CSV)
	for i in range(0, len(nightDay)):
		print(standardizedbaseDataToNightDay[i])
		row = (nightDay[i], standardizedbaseDataToNightDay[i], "" )
		writer.writerow(row)
	CSV.close()

plt.plot(nightDay, label = "Night Day Graphed")
plt.plot(standardizedbaseDataToNightDay, label = "Velocity Data")
plt.legend(loc='lower right')
plt.ylabel("Image Recognition Estimate")
plt.xlabel("Duration of Data Collection (2 Hr 50 Min) ")
plt.title("Velocity Pattern of the ISS Overlayed on the Night, Day \nand Twilight Cycle as observed in Images")
plt.grid(True)
plt.savefig("BaseData_Compared_To_Image_Cycle.png")
plt.show()

"""
plt.plot(baseData)
plt.ylabel("Velocity (Km/S)")
plt.xlabel("Duration of Data Collection (2 Hr 50 Min) ")
plt.title("Velocity of the ISS Collected from \nMay 6th to 7th, 22:53:20 to 01:46:22 UTC 0")
plt.grid(True)
plt.savefig("KMs_Per_Second_Over_2_Hours.png")
plt.show()
"""

#THIS IS THE MOST IMPORTANT GRAPGH! IT SHOWS OUR RESULTS! THE PEAKS KINDA MATCH!! :)
#Creates graph using standerdized fourAvg data
#plt.style.use('dark_background')
plt.plot(oneToZeroFourAvg, label = "Estimated Elevation")
plt.plot(standardizedElevations, label = "True Elevation")
plt.legend(loc='upper left')
plt.ylabel("Elevation (m)")
plt.xlabel("Duration of Data Collection (2 Hr 50 Min) ")
plt.title("True Elevation of Earth Compared to Estimated \nElevation Generated Using Velocity Data")
plt.grid(True)

plt.savefig("Standardized_Elevation_and_Velocity.png")
plt.show()


oneToHundredFourAvg = []
standardize(oneToZeroFourAvg, oneToHundredFourAvg, [0, 100])

oneToHundredElevations = []

standardize(standardizedElevations, oneToHundredElevations, [0, 100])


subtractedAccuracy = []
for i in range(0, len(oneToZeroFourAvg)):
	subtractedAccuracy.append(oneToHundredFourAvg[i] - oneToHundredElevations[i])

subtractedAccuracyNoZero = []
for i in range(0, len(subtractedAccuracy)):
	if subtractedAccuracy[i] > 1 or subtractedAccuracy[i] < -1:
		subtractedAccuracyNoZero.append(subtractedAccuracy[i])

print(subtractedAccuracyNoZero)
print("The average Difference wihtout the zero: " + str((sum(subtractedAccuracyNoZero) / len(subtractedAccuracyNoZero)) ))

print("The average Difference: " + str((sum(subtractedAccuracy) / len(subtractedAccuracy)) ))
plt.plot(subtractedAccuracy)
plt.ylabel("Devation (%)")
plt.xlabel("Duration of Data Collection (2 Hr 50 Min) ")
plt.title("True Elevation Subtracted from Estimated Elevation")
plt.grid(True)
plt.savefig("Guess_True_Accuracy.png")
plt.show()
