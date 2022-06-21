from pathlib import Path
from PIL import Image
from pycoral.adapters import common
from pycoral.adapters import classify
from pycoral.utils.edgetpu import make_interpreter
from pycoral.utils.dataset import read_label_file
from datetime import datetime
import csv


with open("datafile4.csv", "w") as CSV4:
  writer = csv.writer(CSV4)
  header4 = ("ImageNumber", )
  writer.writerow(header4)
CSV4.close()

script_dir = Path(__file__).parent.resolve()

model_file = script_dir/'NightDayTwilight.tflite' # name of model
label_file = script_dir/'labels.txt' # Name of your label file


interpreter = make_interpreter(f"{model_file}")
interpreter.allocate_tensors()
size = common.input_size(interpreter)
labels = read_label_file(label_file)




#Writes to error file in case of error
ErrorCount = 0
Errors = [("calcultaing the number of images"), ("classifying image "), ("writing to classification datafile4")]

def ErrorWrite(message):
  Error_Time = datetime.now()
  with open("datafile3.csv", "a") as CSV3:
    CSV3.write(f"The classify program encountered an error {Errors[message]} at {str(Error_Time)}\n")
  CSV3.close()
  global ErrorCount
  ErrorCount += 1

#Gets the number of images taken during main loop
ImageNumbers = []
with open('datafile2.csv','r') as CSV2:
  plots = csv.reader(CSV2, delimiter=',')
  for row in plots:
    if str(row[0]) != "LoopNumber":
      ImageNumbers.append(row[1])
      print("Added LOOP")
try:
  iteration = (1 + int(ImageNumbers[-1]))
except:
    ErrorWrite(0)
    
    
def ImageClassify():
  for i in range(1, iteration):
    image_file = script_dir/f'Photo{i}.jpg' # Name of image for classification
    image = Image.open(image_file).convert('RGB').resize(size, Image.ANTIALIAS)
    
#   #PLEASE NO ERROR!!!! :) :)
    try:
      common.set_input(interpreter, image)
      interpreter.invoke()
      classes = classify.get_classes(interpreter, top_k=1)
      for c in classes:
        print(f'{labels.get(c.id, c.id)} {c.score:.5f}')
        with open("datafile4.csv", "a") as CSV4:
          try:
            writer = csv.writer(CSV4)
            row4 = (i, (labels.get(c.id, c.id)), (f"{c.score:.5f}") )
            writer.writerow(row4)
            print("Succsesfully wrote to datafile4")

          except:
             Error_Time = datetime.now()
             print("The program encountered an error writing to Image datafile2 at " + str(Error_Time))
             ErrorWrite(2)
    except:
      ErrorWrite(1)
            
