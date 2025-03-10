#serial test
import serial
import matplotlib.pyplot as plt
import numpy as np
from FGConnector import FlightGearConnector
from conversions import ned2lla

#Set your serial ports and baud rate accordingly (must match on microcontroller)
ser = serial.Serial(port='/dev/cu.usbserial-0001',baudrate=9600)
ser2 = serial.Serial(port='/dev/cu.usbmodem1201',baudrate=9600)

#Create FGConnector instance with 5501/5502 ports respectively
FG = FlightGearConnector(5501, 5502)

#Initialize variables
loading = True
loaded = False
idx = 0

#Timestep and number of timesteps (must match on microcontroller)
step = 0.005
nTimesteps = 3000

#Point of origin (XYZ = 0)
#CYYZ runway 33R, change location to your desired airport and runway
lat0_target = np.deg2rad(43.670923)
lon0_target = np.deg2rad(-79.614731)
#MSL altitude (m)
alt0 = 170

#Runway heading (offset by ~10 degrees for FlightGear)
psi = np.deg2rad(-42)

#Downrange distance and XYZ starting point
downrange = 2000
X = downrange*np.cos(psi + np.pi)
Y = downrange*np.sin(psi + np.pi)

#Initial altitude (positive down) and speed
Z = -500
speed = 125

#Empty arrays to store incoming serial values
state = np.zeros(nTimesteps+1)
u_input = np.zeros(nTimesteps+1)
time = np.zeros(nTimesteps+1)

if __name__ == '__main__':
    
    #keep reading serial data
    while loading:
        
        #Read both Serial ports
        value = ser.readline()
        value2 = ser2.readline()
        valueInString = str(value, 'UTF-8')
        valueInString2 = str(value2, 'UTF-8')
        
        #if "STOP" is not received, extract the value, convert to float, assign to array
        if not "STOP" in valueInString:
            values_ESP32 = valueInString.split(",")
            values_UNO = valueInString2.split(",")
            try:
                state[idx] = float(values_ESP32[1])
                u_input[idx] = float(values_UNO[1])
            except IndexError:
                break
            time[idx] = idx*step
            idx+=1
            print(idx)
        
        #Stop reading data if "STOP" is received
        if "STOP" in valueInString:
            loading = False
            loaded = True
        
    #Once data is loaded, plot and pass to FlightGear inputs
    if loaded:
        
        #Plot pitch angle vs time
        plt.subplot(2,1,1)
        plt.plot(time, state)
        plt.xlabel("Time(s)")
        plt.ylabel(r"$\theta$(rad)")
        
        #Plot elevator input vs time
        plt.subplot(2,1,2)
        plt.plot(time,u_input)
        plt.xlabel("Time(s)")
        plt.ylabel(r"$\delta$(rad)")   
        
        #Perform landing sim, fill FlightGear values
        FG.resetInputs()
        for i in range(0, len(time)):
            
            #Get pitch angle, and elevator input (both in rad)
            theta = state[i] 
            delta = u_input[i] 
            
            #Euler's method
            X = X + step*(speed*np.cos(psi)*np.cos(theta))
            Y = Y + step*(speed*np.sin(psi)*np.cos(theta))
            Z = Z + step*(-speed*np.sin(theta))
            
            #Get LLA from XYZ
            P_LLA = ned2lla(X, Y, Z, lat0_target, lon0_target, alt0)
            
            #Pass to FlightGear
            FG.loadInputs(P_LLA[0], P_LLA[1], P_LLA[2], 0, theta, psi, delta)
        
        #Run FlightGear sim
        FG.initializeConnection()
        FG.runSimulator()        
        
    
    
