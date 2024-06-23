#Assignment 0 - Testing Python and FG (completed - please test)

import time
from flightgear_python.fg_if import FDMConnection
import pandas as pd
import math

i = 0

def fdm_callback(fdm_data, event_pipe):
    global i
    #position and orientation
    fdm_data.lat_rad = latValues[i]
    fdm_data.lon_rad = lonValues[i]
    fdm_data.alt_m = hvalues[i]
    fdm_data.phi_rad = phivalues[i]
    fdm_data.theta_rad = thvalues[i]
    fdm_data.psi_rad = psivalues[i] + -3.14
    #FG heading is offset by 10 degrees
    #psi_rad = 0.65 (37 deg) shows up as 47 deg
    #psi_rad = 3.14 (180 deg) shows up as 190 deg
    #psi_rad = 5.14 (294 deg) shows up as 304
    #psi_rad = -0.65 (-37 deg) shows up as 333 deg (323 + 10)
    #psi_rad = -3.14 (180 deg) shows up as 190 deg (180 + 10)
    
    #control surface movements
    fdm_data.elevator = math.sin(time.time())
    fdm_data.left_aileron = math.sin(time.time())
    fdm_data.right_aileron = math.sin(time.time())
    fdm_data.rudder = math.sin(time.time())
    
    i += 1
    if i >= 1035:
        i = 0
    print(hvalues[i] + 20)
    return fdm_data  # return the whole structure

"""
Start FlightGear with `--native-fdm=socket,out,30,localhost,5501,udp --native-fdm=socket,in,30,localhost,5502,udp`
(you probably also want `--fdm=null` and `--max-fps=30` to stop the simulation fighting with
these external commands)
"""
if __name__ == '__main__':  # NOTE: This is REQUIRED on Windows!
    #read values
    data = pd.read_csv("fullTrajectory.csv")
    latValues = data.Latitude*(math.pi/180)
    lonValues = data.Longitude*(math.pi/180)
    hvalues = data.Height
    phivalues = data.Roll
    thvalues = data.Pitch
    psivalues = data.Yaw
    #initialize FG connection and run callback
    fdm_conn = FDMConnection(fdm_version=24)  # May need to change version from 24
    fdm_event_pipe = fdm_conn.connect_rx('localhost', 5501, fdm_callback)
    fdm_conn.connect_tx('localhost', 5502)
    fdm_conn.start()  # Start the FDM RX/TX loop

    while True:
        time.sleep(0.025)
