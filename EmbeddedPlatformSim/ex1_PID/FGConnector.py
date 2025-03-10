#FlightGear Connector class
import time
from flightgear_python.fg_if import FDMConnection
import pandas as pd
import math

class FlightGearConnector:
    def __init__(self, rxPort, txPort):
        #Initialize Inputs
        self.i = 0
        self.latValues = []
        self.lonValues = []
        self.hvalues = []
        self.phivalues = []
        self.thvalues = []
        self.psivalues = []
        self.elevatorvalues = []
        self.rxPort = rxPort
        self.txPort = txPort

    def initializeConnection(self):
        #Initialize FDM Data
        self.fdm_conn = FDMConnection(fdm_version=24)  # May need to change version from 24
        self.fdm_event_pipe = self.fdm_conn.connect_rx('localhost', self.rxPort, self.fdm_callback)
        self.fdm_conn.connect_tx('localhost', self.txPort)
    
    #all angles in rad
    def loadInputs(self, lat, lon, alt, phi, theta, psi, elev):
        self.latValues.append(lat)
        self.lonValues.append(lon)
        self.hvalues.append(alt)
        self.phivalues.append(phi)
        self.thvalues.append(theta)
        self.psivalues.append(psi)
        self.elevatorvalues.append(elev)
    
    def resetInputs(self):
        self.latValues.clear()
        self.lonValues.clear()
        self.hvalues.clear()
        self.phivalues.clear()
        self.thvalues.clear()
        self.psivalues.clear()
        self.elevatorvalues.clear()
        self.i = 0
        
    def fdm_callback(self, fdm_data, event_pipe):
        fdm_data.lat_rad = self.latValues[self.i]
        fdm_data.lon_rad = self.lonValues[self.i]
        fdm_data.alt_m = self.hvalues[self.i]
        fdm_data.phi_rad = self.phivalues[self.i]
        fdm_data.theta_rad = self.thvalues[self.i]
        fdm_data.psi_rad = self.psivalues[self.i]
        fdm_data.elevator = self.elevatorvalues[self.i]
        self.i += 1
        if self.i >= len(self.latValues):
            self.i = 0
        print(self.hvalues[self.i])
        return fdm_data
    
    def runSimulator(self):
        self.fdm_conn.start()   
        while(True):
            time.sleep(0.05)
            
"""
Start FlightGear with `--native-fdm=socket,out,30,localhost,rxPort,udp 
--native-fdm=socket,in,30,localhost,txPort,udp`
"""            
