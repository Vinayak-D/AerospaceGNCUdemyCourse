#run both files

import threading
import subprocess
from FGConnector import FlightGearConnector

if __name__ == "__main__":
    
    #FGConnector(rxPort,txPort,fileName)
    
    flight_1 = FlightGearConnector(5501,5502,"trajectory1.csv")
    flight_2 = FlightGearConnector(5503,5504,"trajectory2.csv")
    
    flight_1_thread = threading.Thread(target=flight_1.runSimulator)
    flight_2_thread = threading.Thread(target=flight_2.runSimulator)
    
    flight_1_thread.start() 
    flight_2_thread.start() 
    
    flight_1_thread.join()
    flight_2_thread.join()

    print("All scripts have finished executing.")