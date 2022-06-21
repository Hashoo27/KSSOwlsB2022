# Obtain the current time `t`
from orbit import ISS
import reverse_geocoder as rg
import matplotlib.pyplot as plt

from time import sleep
from datetime import datetime
from datetime import timedelta

import csv
from pathlib import Path
from math import cos, asin, sqrt, pi

from picamera import PiCamera
camera = PiCamera()
camera.resolution = (1296,972)

StartTime = datetime.now()

#The gap betwwen the data collections
sleepGap = 5

ErrorCount = 0

#Defining the dave path
base_folder = Path(__file__).parent.resolve()
data_file = base_folder/'data.csv'

#Creating datafile
CSV1 = open("datafile1.csv", "w")
CSV1.close()

#Creating datafile
CSV2 = open("datafile2.csv", "w")
CSV2.close()

#Creating datafile
CSV3 = open("datafile3.csv", "w")
CSV3.close()



#Writing headers to datafile
with open("datafile1.csv", "a") as CSV1:
  writer = csv.writer(CSV1)
  header1 = ("LoopNumber", "Date", "Time", "Latitude1", "Longtitude1", "Latitude2", "Longtitude2", "distance", "km/s", "km/hr", "Country", "City", "LatAccuracy", "LongAccuracy")
  writer.writerow(header1)
CSV1.close()

with open("datafile2.csv", "a") as CSV2:
  writer = csv.writer(CSV2)
  header2 = ("LoopNumber", "ImageNumber", "Date", "Time", "Latitude2", "Longtitude2", "Country", "City", "LatAccuracy", "LongAccuracy")
  writer.writerow(header2)
CSV2.close()

with open("datafile3.csv", "a") as CSV3:
  CSV3.write(f"The program started at {StartTime}\n")
CSV3.close()



#Defining funtion to calculate distance between 2 GPS coordinates
#ERROR: LA2
def distance(lat1, lon1, lat2, lon2):
  try:
    # ERROR: Pi into string
    p = pi/180
  
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return(12742 * asin(sqrt(a))) #2*R*asin...
  except:
    ErrorWrite(0) 

#Defining Funtion to get current time
def Time():
    Current_Time = datetime.now().strftime("%H:%M:%S:%f")
    print(Current_Time)
    return(Current_Time)

#Defining Funtion to get current time
def Date():
    Current_Date = datetime.now().strftime("%d/%m/%Y")
    print(Current_Date)
    return(Current_Date)

Time()

# Funtion to compute the coordinates of the Earth location directly beneath the ISS
def GetLocation():
  try:
    global location
    location = ISS.coordinates()
  except:
    ErrorWrite(1)

def Convert(angle):
  try:

    sign, degrees, minutes, seconds = angle.signed_dms()
  
  
    exif_angle = f'{degrees:.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10'
  
    return sign < 0, exif_angle
  except:
    ErrorWrite(2)


def CaptureImage(camera, ImagePath):
  #Attempts to add EXIF data to image 
  try:
    #Use `camera` to capture an `image` file with lat/long EXIF data.
    GetLocation()

    # Convert the latitude and longitude to EXIF-appropriate representations
    south, exif_latitude = Convert(location.latitude)
    west, exif_longitude = Convert(location.longitude)

    # Set the EXIF tags specifying the current location
    camera.exif_tags['GPS.GPSLatitude'] = exif_latitude
    camera.exif_tags['GPS.GPSLatitudeRef'] = "S" if south else "N"
    camera.exif_tags['GPS.GPSLongitude'] = exif_longitude
    camera.exif_tags['GPS.GPSLongitudeRef'] = "W" if west else "E"
  #Writes to datafile in case of error
  except:
    Error_Time = datetime.now()
    print("The program encountered an error adding EXIF tags to images at " + str(Error_Time))
    ErrorWrite(3)
    
  # Tries to Capture the image
  try:
    camera.capture(ImagePath)
    print("Image Captured")
    
  #Writes to datafile if image capture fails
  except:
    ErrorWrite(4)


    
# 0 == distance Calculation, 1 == Getting Location, 2 == Converting, 3 == Adding EXIF, 4 == Capturing Image, 5 == Writing DataFile2, 6 == Writing DataFile1, 7 == Main loop
Errors = [("calculating the distance travelled by the ISS. The error was encountered"),("getting location of the ISS"), ("Converting Coordinate Angles"), ("adding EXIF tags to images"), ("capturing images"), ("writing to Image datafile2"), ("writing to main datafile1"), ("during main loop")]

#Writes to error file in case of error
def ErrorWrite(message):
  Error_Time = datetime.now()
  with open("datafile3.csv", "a") as CSV3:
    CSV3.write(f"The main program encountered an error {Errors[message]} at {str(Error_Time)}\n")
  CSV3.close()
  global ErrorCount
  ErrorCount += 1


LoopTime = datetime.now

LoopNumber = 0
ImageNumber = 0

LoopTime = datetime.now()

while (LoopTime < (StartTime + timedelta(minutes = 170))):
  LoopTime = datetime.now()

  LoopNumber += 1
  try:
    GetLocation()
    lat1, long1 = location.latitude.degrees, location.longitude.degrees

    sleep(sleepGap)

    GetLocation()
    LoopTime = datetime.now()
    lat2, long2 = location.latitude.degrees, location.longitude.degrees

    #Calculates the distance travelled in the time between 2 readings
    distanceTravelled = distance(lat1, long1, lat2, long2)

    #Calculates the average velocity of the ISS in between 2 readings in km/hr
    calculatedVelocityHr = ((distanceTravelled/sleepGap)*3600)
    #Calculates the average velocity of the ISS in between 2 readings in km/s
    calculatedVelocitySec = ((distanceTravelled/sleepGap))
    
    #Gets the nearest city using latirude and longtitude.
    ReverseCoordinates = (lat2, long2)
    Nearest_City = rg.search(ReverseCoordinates)

    #Takes a Picture every 5 cycles
    if (LoopNumber % 3 == 0):
      ImageNumber += 1
      CaptureImage(camera,f"{base_folder}/Photo{ImageNumber}.jpg")

      with open("datafile2.csv", "a") as CSV2:
        try:
          writer = csv.writer(CSV2)
          row2 = (LoopNumber, ImageNumber, Date(), Time(), lat2, long2, Nearest_City[0]["cc"], Nearest_City[0]["name"], (abs(float(lat2) - float(Nearest_City[0]["lat"]))), (abs(float(long2) - float(Nearest_City[0]["lon"]))))
          writer.writerow(row2)
          print("Succsesfully wrote to datafile2")

        except:
          Error_Time = datetime.now()
          print("The program encountered an error writing to Image datafile2 at " + str(Error_Time))
          ErrorWrite(5)

        finally:
          CSV2.close()

    with open("datafile1.csv", "a") as CSV1:
      
      try:
        writer = csv.writer(CSV1)
        row1 = (LoopNumber, Date(), Time(), lat1, long1, lat2, long2,distanceTravelled, calculatedVelocitySec, calculatedVelocityHr, Nearest_City[0]["cc"], Nearest_City[0]["name"], (abs(float(lat2) - float(Nearest_City[0]["lat"]))), (abs(float(long2) - float(Nearest_City[0]["lon"]))))
        
        writer.writerow(row1)
        print("Succsesfully wrote to datafile1")
        
      except:
        Error_Time = datetime.now()
        print("The program encountered an error writing to main datafile1 at " + str(Error_Time))
        ErrorWrite(6)
        
      finally:
        CSV1.close()

  except:
    ErrorWrite(7)

import classify

while (LoopTime < (StartTime + timedelta(minutes = 177))):
  classify.ImageClassify()
  break

while (LoopTime < (StartTime + timedelta(minutes = 179))):
  date = []
  velocity = []
  with open('datafile1.csv','r') as CSV1:
    plots = csv.reader(CSV1, delimiter=',')
    for row in plots:
      if str(row[0]) != "LoopNumber":
        date.append(row[0])
        velocity.append(row[8])
  plt.plot(date, velocity, label='velocity')
  #plt.plot(date, temprature, label = "Temprature")
  plt.xlabel('Date/Time')
  plt.ylabel('Velocity (Km/hr)')
  plt.title('This is a test')
  #plt.title('Humidity of the International Space Station \n From 18:00 to 21:00 on April 18, 2021')
  plt.legend()
  plt.savefig('Velocity.png')
  break



print(f"The program succsesfully ended at {datetime.now()}")
print(f"The main program encountered {ErrorCount} errors during main loop")

with open("datafile3.csv", "a") as CSV3:
  CSV3.write(f"The program succsesfully ended at {datetime.now()}\n")
  CSV3.write(f"The main program encountered {ErrorCount} errors during main loop")
CSV3.close()
