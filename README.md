# Remote Environment Controller for  Experiments in Extreme Environments
Observing biological systems, animals, traffic or the evolution of cities in their natural environment requires researchers to travel to remote places. Field trips to these distant locations are often limited in time, expensive, or even dangerous. Here, we build an autonomous environment observer that once installed monitors key parameters that are essential for our research.
Our aim is to establish a sensor platform that is autonomous (i.e. solar powered) and able to transmit data and receive instructions remotely. Rather than targeting a single application, we build a generic sensor platform that can be used for a wide range of applications and can be easily adapted. Initially we test our system in a student vegetable garden where the sensor platform will be tested and simple measurements such as soil moisture, UV intensity, temperature, humidity, camera etc. are taken. The main outcome of this project will be a field tested generic sensor platform that can be easily adapted for a wide range of tasks. 

The below figure illustrates the data and power flow of the system:
![alt text](https://github.com/pab96/27_Remote-Environment-Controller-for-Experiments-in-Extreme-Environments/blob/master/LogicStructureRemoteSens.png)
In short, energy from a solar panel is feed into a battery. The battery powers the main processor (i.e. a raspberry pi). However, to save power the pi is only swtched on periodically by an arduini which requires significantly less enery to run and it can simultaniously monitor the battery voltage to prevent deep battery discharge and only swith on when the battery is sufficiently charged. The pi then read data from the sensors after the signal is converted from analog to digital. Finally the data is transmitted via wifi or the GSM (at locations without wifi) and can then be monitored from anywhere in the world with a PC.

The documentation is structured into several independent sub components which include:
* Solar Power and Batteries
* Processor (Raspberry Pi)
* Use of an external timer circuit to save power
* Choice of sensors and how to connect them
* Data transmission
* Mounting and weather resistant casing
* Data display and storage
* Future work

## What you need:
|  Component | Component Details |
| --- | --- |
| Solar panel and 12V battery charger | (RS Stock No.706-7918) |
| Battery | 12V Lead Acid Battery, 1.2Ah (RS Stock No.614-2447) |
| Arduino |Arduino Pro Mini |
|Arduino Uno with USB connection cable| Arduino Uno
| Raspberry Pi and power cable |Raspberry Pi 2B |
|USB to usb micro cable| |
|SD card|16GB Micro SD Card with NOOBS for Raspberry Pi (Onecall Order Code:SC14027 http://onecall.farnell.com/transcend/tsraspi10-16g/memory-microsd-16gb-noobs/dp/SC14027)|
|Voltage Converter| Car battery 12V to 5V USB converter (RS Stock No.814-6261)|
| USB Wifi Adapter| (RS Stock No.760-3625, http://uk.rs-online.com/web/p/wireless-adapters/7603625/)
| Camera |Raspberry Pi Camera V2 Camera Module (RS Stock No.913-2664) |
| Power MOSFET |N-channel MOSFET, 5.6 A, 100 V (RS Stock No.708-5134) |
| Soil Moisture Sensor|(Sparkfun SEN-13637 (https://www.sparkfun.com/products/13637)) |
| UV Sensor |(Sparkfun SEN-12705 https://www.sparkfun.com/products/retired/12705 |
| Air Contaminants Gas Sensor |Figaro TGS2600-B00 (RS Stock No.538-9960 ) |
| Temperature Sensor |Texas Instruments LM35DZ/NOPB (RS Stock No.922-4836) |
| Light Dependent Resistor| (RS Stock No.914-6710)|
|5x 1kOhm Resistor| |
|5.1 MOhm Resistor||
|3x 100 kOhm Resistor||
|1 MOhm Resistor||
|9V Battery||
|Bird House||
|40 Pin Rainbow Color Ribbon Cable for Raspberry Pi||
|Male andFemale Single Row Square Pin Header Strip||

Additionally mouse, keyboard, PC screen with VGA (or with VGA/HDMI converter), breadboard, lots of wires, a multimeter is always useful, soldering board, soldering wire and a soldering iron, silicone or super glue, screws and nuts, screwdrivers, a drill. 

## Power Management
Data recording is only required every hour or so. In the intervalls in between the Pi can be switched off which saves a lot of power.   The pi sleep mode requires too much power and even if the pi is off the sensors would drain power from the pi. Thus, an external timer device is used which cuts the power to the pi and only switches on peridiotically. As external timer we decided to use an Arduino pro mini, because it can be modifyed to use very lowe current (i.e. a few nA). Here are the tricks on reducing arduino power consumption and how to run the periodic switching program. Additionally we added a battery voltage sensor to check that is is save to switch on the pi i.e. if a lead acid battery is run below 11.8V it damages the battery therefore deep discharge should be avoided.

Using the arduino pro mini First install Arduino IDE. You can use an FTDI device to programm the mini. I tried with the one from sparkfun but no matter what I did my PC wouldn't recognice the driver. So I gave up and found a much better otion instead! You can programm the arduino pro mini with a normal Arduino Uno (the one where you can take out the ATMEGA328P), this worked first time I tried! So I recommend you use that option it also spares you from buying an FTDI, rather buy an arduino uno if you don't have one, I'm sure you'll find use for that later. [Here](http://www.instructables.com/id/Program-Arduino-Pro-Mini-Using-Arduino-Uno/) is an excellent tutorial on how to programm the arduino pro mini using the arduino uno. In short you need to take out the ATMEGA328P from the Uno, then connect Uno ground to pro mini ground, the Uno 5V pin to VCC on the pro mini and the Rx and Tx pins as well as the reset pin from Uno to the pro mini. Then go to the Arduino IDE -> Tools-> Board -> Arduino Pro Mini and make sure you have the corret port enabled. Then as usual just upload the program to the Uno which will then go to the pro mini and it works, MAGIC! (Sometimes still PC does not recognise port, try deplug usb with arduino and just uploading it several times at some stage it will work). Before you upload the program arduinoProMiniPowerTimer to the arduino you need to download the [LowPower.h library](https://github.com/rocketscream/Low-Power) i.e. download the whole folder and save it on your disk (i.e. C:\Program Files (x86)\Arduino\libraries). For the low power settings we are following [this guide:](http://www.home-automation-community.com/arduino-low-power-how-to-run-atmega328p-for-a-year-on-coin-cell-battery). I.e. to sigificantly reduce power consumption of the pro mini we use the low power command to put the arduino to sleep. The command LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF) sets the arduino to sleep, max time for this is 8 sec after which the arduino just switches on for a couple of mili seconds and goes to sleep again this is reapeated until 1h has passed. Second the power LED of the arduino pro mini was scractched out with a small screw driver. During the sleep interval the arduino draws 0.06mA from the 9V battery and during the on times it draws 18mA. The on time is really just a few milli seconds so on average the current drawn is close to the 0.06mA. The arduino pro mini is also measuring the lead acid battery voltage through a series of large resistors (to keep the current and power consumer by this low) that devide the voltage of the battery into something between 0 and 3.3V such that both the pi and the arduino can read it. If the lead acid batery volatge drops below 11.5V the power to the pi is not switched on to prevent a deep discharge of the lead acid battery.

The below figure shows how to connect everything up.  
![alt text](https://github.com/pab96/27_Remote-Environment-Controller-for-Experiments-in-Extreme-Environments/blob/master/GardenObserverAll_v2_schemMod.png)
The 9V battery is powering the arduino pro mini through the raw pin which can take volatges up to 12V but no more (I tried connecting the 12V car battery to the arduino raw pin... the result was SMOKY! #NotAGoodIdea)! A simple voltage devider was made with a 5.1MOhm resistor and three 100kOhm resistors and a 1MOhm resistor such that R_1=5.1Mohm and R_2=1M+3*100k=1.3Mohm ->From measuring the voltage over R_2 the battery voltage can be calculated V_battery=V_measured*(R_1+R_2)/R_2. This devides the 12V into something the arduino pro can read withits analogue pins. The programm then switches the power mosfet on whenever 1h has passed and the battery voltage is above 11.5V. Switching the power mosfet on means that the current can flow from the battery battery through the pi to the battery negative. It's important to hook the mosfet up to the negative leg of the battery and not the positive as it would not work on the positive leg. 

## Solar Power and Batteries:
Considering that the pi could draw up to 1A, we decided to use a lead acid car battery. These are fairly cheap, have a long lifetime, can be recharged and a large current can be drawn from them. The solar panel we used here is very handy because it comes directly with a 12V lead acid battery charger. Below is a picture of this solar panel module connected to the battery. Since we integrated the solar panel on a bird house, we cut off all the unesscary plastic of the solar panel kit and attached it to the roof of the bird house. 
![alt text](https://github.com/pab96/27_Remote-Environment-Controller-for-Experiments-in-Extreme-Environments/blob/master/SolarPanelBeforeAndAfterDismount.png)
Here is a very rough estimation of how much energy we get from the panel and how much we need. 
* On an overcast September day at 10am the solar panel yielded about 20mA and about 20V i.e. 400mW. In winter we might only get 5h daylight so let's say we can generate 2Wh/day. 
* The arduino pro mini consumers (let's be consverative) 0.1mA @ 9V -> 0.9mW x 24h -> 21.6mWh
* The raspberry pi with sensors consumes about 500mA @ 5V. The voltage converter is probaply very innefficient let's guess 50%. The pi is only switched on for 1min every hour. So in total 0.5 x 5 x 1/0.5 x 24/60 =2Wh/day
So we consume ~2Wh/day and on a cloudy day in winter produce 2Wh/day. That means the small solar panel should just be enough to get over the winter. 

## Multiplexing and analogue to digital conversion (ADC):
The pi can only input digital data, however the sensor data is analog. Therefore we use a MCP3008 analog to digital converter (ADC) to supply the pi with the data in the correct format. The MCP3008 has 8 input channels, thus 8 sensors can be connected to it and read out by the pi. 
Connect MCP3008 as follows (More info on setting up MCP3008 [here:](https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008)):
* MCP3008 VDD to Raspberry Pi 3.3V
* MCP3008 VREF to Raspberry Pi 3.3V
* MCP3008 AGND to Raspberry Pi GND
* MCP3008 DGND to Raspberry Pi GND
* MCP3008 CLK to Raspberry Pi pin 18
* MCP3008 DOUT to Raspberry Pi pin 23
* MCP3008 DIN to Raspberry Pi pin 24
* MCP3008 CS/SHDN to Raspberry Pi pin 25
Channel 0-7 will then read voltages from 0...3.3V and give a signal 0...1023 accordingly.

## Processor
We want to be able to possibly track a large number of sensors, take pictures and access a wifi. Doing this with an arduino will require quite a few boards and thus we decided to use an rasperry pi as the central processing unit. This comes at the disadvantage that a pi requires quite a lot of power, however we will overcome this by only switchen the pi on for limited periods.
First of all set up your pi. If you have never done this follow this quide: https://www.raspberrypi.org/app/uploads/2012/04/quick-start-guide-v2_1.pdf
Carefully follow the instuctions in the file "SettingUpThePi" to set up github on the pi as well as change to correct time zone, make a programm that is executed upon powering the pi which includes the sensor read commands and data transmission commands and setting up the SPI to be able to use the MCP3008. Also check the camera.py file on how to set up the camera.   


## License

A short snippet describing the license (MIT, Apache, etc.) you have chosen to use
