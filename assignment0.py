import time
from flightgear_python.fg_if import FDMConnection
import pandas as pd
import math
 
class FlightGearConnector:
    def __init__(self):
        # Initialize variables
        self.latValues = []
        self.lonValues = []
        self.hvalues = []
        self.phivalues = []
        self.thvalues = []
        self.psivalues = []
        self.i = 0
 
        # Load data
        self.load_data()
 
        # Initialize FlightGear connection
        self.fdm_conn = FDMConnection(fdm_version=24)
        self.fdm_event_pipe = self.fdm_conn.connect_rx('localhost', 5501, self.fdm_callback)
        self.fdm_conn.connect_tx('localhost', 5502)
        
    def load_data(self):
        # Read values from CSV
        data = pd.read_csv("fullTrajectory.csv")
        self.latValues = data.Latitude * (math.pi / 180)
        self.lonValues = data.Longitude * (math.pi / 180)
        self.hvalues = data.Height
        self.phivalues = data.Roll
        self.thvalues = data.Pitch
        self.psivalues = data.Yaw
 
    def fdm_callback(self, fdm_data, event_pipe):
        # Position and orientation
        fdm_data.lat_rad = self.latValues[self.i]
        fdm_data.lon_rad = self.lonValues[self.i]
        fdm_data.alt_m = self.hvalues[self.i]
        fdm_data.phi_rad = self.phivalues[self.i]
        fdm_data.theta_rad = self.thvalues[self.i]
        fdm_data.psi_rad = self.psivalues[self.i] - 3.14  # Correcting the psi offset
 
        # Control surface movements
        fdm_data.elevator = math.sin(time.time())
        fdm_data.left_aileron = math.sin(time.time())
        fdm_data.right_aileron = math.sin(time.time())
        fdm_data.rudder = math.sin(time.time())
 
        self.i += 1
        if self.i >= len(self.latValues):
            self.i = 0
 
        print(self.hvalues[self.i] + 20)
        return fdm_data  # Return the whole structure
 
    def start(self):
        self.fdm_conn.start()  # Start the FDM RX/TX loop
        while True:
            time.sleep(0.025)
 
if __name__ == '__main__':
    # Create an instance of FlightGearConnector
    fg_connector = FlightGearConnector()
    
    # Start the FlightGear connection
    fg_connector.start()