#FlightGear Connector class
import time
from flightgear_python.fg_if import FDMConnection
import pandas as pd
import math

class FlightGearConnector:
    def __init__(self, rxPort, txPort, fileName):
        #Initialize Inputs
        self.i = 0
        self.latValues = []
        self.lonValues = []
        self.hvalues = []
        self.phivalues = []
        self.thvalues = []
        self.psivalues = []
        self.data = []
        self.rxPort = rxPort
        self.txPort = txPort
        self.fileName = fileName
        #Load Inputs
        self.loadInputs()
        #Initialize FDM Data
        self.fdm_conn = FDMConnection(fdm_version=24)  # May need to change version from 24
        self.fdm_event_pipe = self.fdm_conn.connect_rx('localhost', self.rxPort, self.fdm_callback)
        self.fdm_conn.connect_tx('localhost', self.txPort)
    
    def loadInputs(self):
        self.data = pd.read_csv(self.fileName)
        self.latValues = self.data.Latitude
        self.lonValues = self.data.Longitude
        self.hvalues = self.data.Height
        self.phivalues = self.data.Roll
        self.thvalues = self.data.Pitch
        self.psivalues = self.data.Yaw     
        
    def fdm_callback(self, fdm_data, event_pipe):
        fdm_data.lat_rad = 43.6817*(math.pi/180)
        fdm_data.lon_rad = -79.61450000000001*(math.pi/180)
        fdm_data.alt_m = self.hvalues[self.i]
        fdm_data.phi_rad = self.phivalues[self.i]
        fdm_data.theta_rad = self.thvalues[self.i]
        fdm_data.psi_rad = self.psivalues[self.i]
        self.i += 1
        if self.i >= len(self.data):
            self.i = 0
        print(self.hvalues[self.i])
        return fdm_data
    
    def runSimulator(self):
        self.fdm_conn.start()   
        while(True):
            time.sleep(0.025)
            
"""
Start FlightGear with `--native-fdm=socket,out,30,localhost,rxPort,udp 
--native-fdm=socket,in,30,localhost,txPort,udp`
"""            
