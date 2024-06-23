#Assignment 1 - Coordinate Transforms (TODO)

import time
from flightgear_python.fg_if import FDMConnection
import math
import numpy as np
from conversions import ned2lla, lla2ned
d2r = np.deg2rad
import matplotlib.pyplot as plt

i = 0
def fdm_callback(fdm_data, event_pipe):
    global i
    #position and orientation
    fdm_data.lat_rad = latValues[i]
    fdm_data.lon_rad = lonValues[i]
    fdm_data.alt_m = 500
    fdm_data.phi_rad = 0
    fdm_data.theta_rad = 0
    fdm_data.psi_rad = psi
    i += 1
    if i >= len(latValues) - 1:
        i = 0    
    return fdm_data  # return the whole structure

def generateTrajectory(lat0_target, lon0_target, alt0, psi):
    time = 5
    dT = 0.01
    x = 0
    y = 0
    xcalc = [0]
    ycalc = [0]
    xtrue = [0]
    ytrue = [0]
    D = -383
    speed = 200
    theta = 0
    lat_values = [lat0_target]
    lon_values = [lon0_target]
    for i in range(int(time/dT)):
        
        #Student Section-------------------------------------------------------------------------------------------
        
        #Update timestep (see assignment1.png)
        x = x + dT*(0) #replace '0', hint use math.sin/math.cos
        y = y + dT*(0) #replace '0'
        
        xtrue.append(0) #replace
        ytrue.append(0) #replace
        
        #Convert to LLA (call the appropriate function from 'conversions')
        P_LLA = 0 #replace '0'
        lat_values.append(0) #replace '0'
        lon_values.append(0) #replace '0'
        
        #Convert back to NED for comparison (Call the appropriate function from 'conversions')
        P_NED = 0 #replace
        
        #End Student Section---------------------------------------------------------------------------------------
        
        xcalc.append(P_NED[0])
        ycalc.append(P_NED[1])
    return [lat_values, lon_values, xtrue, ytrue, xcalc, ycalc]

if __name__ == '__main__':
    
    #Point of Origin LLA
    lat0_target = d2r(43.67458)
    lon0_target = d2r(-79.66346)
    alt0 = 117
    psi = d2r(50)
    #Generate trajectory
    trajectory = generateTrajectory(lat0_target, lon0_target, alt0, psi)
    latValues = trajectory[0]
    lonValues = trajectory[1]
    #Plot NED values
    plt.figure('NED coordinates')
    plt.plot(trajectory[2], trajectory[3], 'r-', label = 'true')
    plt.plot(trajectory[4], trajectory[5], 'b--', label = 'calculated')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.title('NED Coordinates')
    
    #FG callback
    fdm_conn = FDMConnection(fdm_version=24)  # May need to change version from 24
    fdm_event_pipe = fdm_conn.connect_rx('localhost', 5501, fdm_callback)
    fdm_conn.connect_tx('localhost', 5502)
    fdm_conn.start()  # Start the FDM RX/TX loop    
    while(True):
        time.sleep(0.025)
