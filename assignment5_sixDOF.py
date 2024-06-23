#Assignment 5 - Six Degrees of Freedom (completed)

import time
from flightgear_python.fg_if import FDMConnection
import pandas as pd
import math
import numpy as np
from conversions import ned2lla
d2r = np.deg2rad

def fdm_callback(fdm_data, event_pipe):
    global i
    #position and orientation
    fdm_data.lat_rad = lat[i]
    fdm_data.lon_rad = lon[i]
    fdm_data.alt_m = height[i]/10
    fdm_data.phi_rad = phi[i]
    fdm_data.theta_rad = theta[i]
    fdm_data.psi_rad = psi[i]
    fdm_data.alpha_rad = alpha[i]
    fdm_data.beta_rad = beta[i]
    fdm_data.v_north_ft_per_s = u[i]*3.3
    fdm_data.v_east_ft_per_s = v[i]*3.3
    fdm_data.v_down_ft_per_s = w[i]*3.3
    
    #control surface movements
    fdm_data.elevator = elevR[i]
    fdm_data.left_aileron = canard[i]
    fdm_data.right_aileron = canard[i]
    fdm_data.rudder = rudder[i]
    fdm_data.left_flap = flapL[i]
    fdm_data.right_flap = flapR[i]

    i += 1
    print(float(i/len(lat)*100))
    if i >= len(lat)-1:
        i = 0
    return fdm_data  # return the whole structure

"""
Start FlightGear with `--native-fdm=socket,out,30,localhost,5501,udp --native-fdm=socket,in,30,localhost,5502,udp`
(you probably also want `--fdm=null` and `--max-fps=30` to stop the simulation fighting with
these external commands)
"""
if __name__ == '__main__':  # NOTE: This is REQUIRED on Windows!

    #Point of Origin LLA
    lat0_target = d2r(43.67458)
    lon0_target = d2r(-79.66346)
    alt0 = 117

    #read values    
    data = pd.read_csv("trajectory.csv")
    u = data.u
    v = data.v
    w = data.w
    VT = data.VT
    phi = data.phi
    theta = data.theta
    psi = data.psi
    N = data.XE
    E = data.YE
    D = data.ZE
    elevR = data.elevR
    elevL = data.elevL
    flapR = data.flapR
    flapL = data.flapL
    canard = data.canard
    rudder = data.rudder
    alpha = data.alpha
    beta = data.beta
    
    #calculate NED trajectory
    lat = [lat0_target]
    lon = [lon0_target]
    height = [alt0 - D[0]]
    for i in range(len(N)):
        P_LLA = ned2lla(N[i], E[i], D[i], lat0_target, lon0_target, alt0)
        lat.append(P_LLA[0])
        lon.append(P_LLA[1])
        height.append(P_LLA[2])

    #initialize FG connection and run callback
    fdm_conn = FDMConnection(fdm_version=24)  # May need to change version from 24
    fdm_event_pipe = fdm_conn.connect_rx('localhost', 5501, fdm_callback)
    fdm_conn.connect_tx('localhost', 5502)
    fdm_conn.start()  # Start the FDM RX/TX loop

    while True:
        time.sleep(0.025)
