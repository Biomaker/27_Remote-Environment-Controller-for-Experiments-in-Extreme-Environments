# Reading from the MCP3008 and stroing the date
# Execute me with: sudo python readAndStoreSensorData.py
import time
from time import sleep,localtime, strftime
import sys
import numpy as np
import os

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

import RPi.GPIO as GPIO #For pulling pins high/low

fileAndfolderPathStoreData="/home/pi/BioMaker/GitHubGardenObserver/Data/GardenObserver_SensorData.txt"

# Software SPI configuration:
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

#GPIO.setup(21, GPIO.OUT)
#GPIO.output(21, GPIO.HIGH)
print("Sensors board is being powered...")


## Sensor data sampling
print('Reading MCP3008 values, press Ctrl-C to quit...')
samplingTime=1; # time through which sensor data is sampled
samplingInterval=0.25; # sample every 0.25sec
samplingCount=0
allSamplingValues=d = np.zeros((samplingTime/samplingInterval+1,8)) # Initialising a zeros matrix
while samplingCount<=samplingTime/samplingInterval:
    # Read all the ADC channel values in a list.
    for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
        allSamplingValues[samplingCount][i]= mcp.read_adc(i)
    samplingCount += 1
    time.sleep(samplingInterval)

#GPIO.output(21, GPIO.LOW)
print("Sensor reading done power shut off from sensor boad")

## Sensor data processing mean and std
averageSensorData=np.mean(allSamplingValues,axis=0)
stdSensorData=np.std(allSamplingValues,axis=0)
#print(allSamplingValues) # Print Raw values
#print("Averaged values:")
#print(averageSensorData)
#print(stdSensorData)
##sys.stdout.write(strftime("%d.%m.%Y %H:%M:%S", localtime())) # use sys.stout.write to print in same line as command below
print(' | {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*np.around(averageSensorData,decimals=1)))
##print(' | {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*np.around(stdSensorData,decimals=2)))


## Converting MCP3008 value to respective Units
averageSensorData=np.multiply(averageSensorData, 3.3/1023) # Converting all values to Volt

# MCP3008 Channel 0: UV Sensor
averageSensorData[0]=0.125*averageSensorData[0]+1  #UV intensity @365nm in [mW/cm^2] 1-3 is minimal UV, 3-4 is low, 5-6 is moderate, 7-9 is high, 10-12 is very high exposure

# MCP3008 Channel 1: Battery Voltage: Batterie is on a voltage devider with a R_1=5.1Mohm and R_2=1M+3*100k=1.3Mohm -> Voltage over R_2: V_measured=V_2=V_battery*R_2/(R_1+R_2)-> V_battery=V_measured*(R_1+R_2)/R_2
# Voltage could also be converted in % charged. 12.7V means 100% charged, 11.9 means discharged
averageSensorData[1]=averageSensorData[1]*(5.1+1.3)/1.3  # Converting to %, 0 being empty 100% being charged



# MCP3008 Channel 4: Thermometer LM35DZ V_out=10mV/degC*T
averageSensorData[4]=averageSensorData[4]/0.01  # Temp in [DegC]

# MCP3008 Channel 5: TGS 2600 Air Contaminants: R_S=(5V/V_out-1)* R_load /R_referenceReading
# Lower values than 100% mean air is contaminated with CO, Methane, Isobutahnol, Hydrogen, Ethanol
averageSensorData[5]=(5/averageSensorData[5]-1)*1000/25000*100 # R_referencereading was done in room with open window 20degC August [%]

# MCP3008 Channel 7: Soil Moisture Sensor. Was calibrated by hand: 0.92V when fully coverd in water, 0V is in air dry. Will read [%] water 0% meaning dry and 100% fully wet!
averageSensorData[6]=averageSensorData[6]/1.15*100#(1-(averageSensorData[2]-1.325)/(3.3-1.325))*100  # Converting to %, 0 being dry, 100% being immersed in water

# MCP3008 Channel 8: Light Dependent Resistor LDR
averageSensorData[7]=averageSensorData[7]/3.3*100  # Converting to % 2% just enough to see, above 8% you can see well, 30% ambient in shadow, 90% quite bright

# MCP3008 Channel 0: Adjustable Resistor
# averageSensorData[0]=averageSensorData[0]/3.3*100  # Converting to %

## preparing sensor data for storage
print("Date,Time | Avg_Sens_1 |Avg_Sens_2 |Avg_Sens_3 |Avg_Sens_4 |Avg_Sens_5 |Avg_Sens_6 |Avg_Sens_7 |Avg_Sens_8 ||Std_Sens_1 |Std_Sens_2 |Std_Sens_3 |Std_Sens_4 |Std_Sens_5 |Std_Sens_6 |Std_Sens_7 |Std_Sens_8 |")
print('-' * 57)
sensorDataToBeSaved=strftime("%d.%m.%Y %H:%M:%S", localtime()) # Date and Time
sensorDataToBeSaved += ' | {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4}'.format(*np.around(averageSensorData,decimals=3)) # The sensor data avaerage values to 1 decimal place
sensorDataToBeSaved += ' || {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4}'.format(*np.around(stdSensorData,decimals=3))    # The sensor data std values to 2 decimal place
print(sensorDataToBeSaved)

## Writing to Sensor Storage File
fileHandle=0;
if os.path.isfile(fileAndfolderPathStoreData):  #check if file already exists
    fileHandle = open(fileAndfolderPathStoreData,"a") #if already exist go to "a"= appendix mode and new text will be added below
    fileHandle.write("\n")
else:
    fileHandle = open(fileAndfolderPathStoreData,"a")
    fileHandle.write("Date Time | Avg_Sens_1 |Avg_Sens_2 |Avg_Sens_3 |Avg_Sens_4 |Avg_Sens_5 |Avg_Sens_6 |Avg_Sens_7 |Avg_Sens_8 ||Std_Sens_1 |Std_Sens_2 |Std_Sens_3 |Std_Sens_4 |Std_Sens_5 |Std_Sens_6 |Std_Sens_7 |Std_Sens_8 |") 
    fileHandle.write("\n")
    fileHandle.write('-' * 100)
    fileHandle.write("\n")

fileHandle.write(sensorDataToBeSaved)
fileHandle.close() 
print("Sensor data successfully saved locally")


