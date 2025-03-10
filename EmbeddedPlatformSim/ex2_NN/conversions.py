#Coordinate conversions (TODO)

import numpy as np
d2r = np.deg2rad

#Latitude, Longitude, Altitude to North East Down Conversion
def lla2ned(latrad, lonrad, alt, lat0_target, lon0_target, alt0):
    
    # Inputs  latrad: latitude of waypoint (rad)
    #         lonrad: longitude of waypoint (rad)
    #         alt: altitude of waypoint (m) 
    #         lat0_target : Origin latitude (rad)
    #         lon0_target : Origin longitude (rad)
    #         alt0_target : Origin altitude (m)
    # Output  P_ned: NED position (m) 
    
    # WGS84 spheroid constants
    a = 6378137
    b = 6356752.3142
    f = -(b/a)+1
    
    # Convert ECEF coordinates to latitude, longitude and altitude above WGS-84
    lat = latrad
    lon = lonrad
    
    # Find NED waypoint coordinates
    # The eccentricity (e) is sqrt(2f-f^2)
    
    lat0 = lat0_target
    lon0 = lon0_target
    
    #Student Section, Complete RN_init, RM_init, dN_init, dE_init-----------------------------------------------------------------------
    
    RN_init = 0 #Replace '0'
    RM_init = 0 #Replace '0'
    dN_init = 0 #Replace '0'
    dE_init = 0 #Replace '0'
    N = dN_init
    E = dE_init
    D = alt0-alt
    
    #End Student Section ---------------------------------------------------------------------------------------------------------------
    
    P_ned = (N,E,D)
    
    return P_ned

#North East Down to Latitude, Longitude, Altitude Conversion (completed)
def ned2lla(N, E, D, lat0_target, lon0_target, alt0):
    
    # Inputs  N: North position {x} (m)
    #         E: East position {y} (m)
    #         D: Down position {z} (m) 
    #         lat0_target : Origin latitude (rad)
    #         lon0_target : Origin longitude (rad)
    #         alt0_target : Origin altitude (m)
    #
    # Output  P_LLA: LLA position (m)    
    
    # Required constants
    a = 6378137;
    b = 6356752.3142;
    e_sqr = (a**2-b**2)/a**2;
    e2_sqr = (a**2-b**2)/b**2; 
    
    #NED to ECEF rotation matrix using the origin 
    R_NEF = np.zeros([3,3])
    R_NEF[0,0] = -np.sin(lat0_target)*np.cos(lon0_target)
    R_NEF[0,1] = -np.sin(lon0_target)
    R_NEF[0,2] = -np.cos(lat0_target)*np.cos(lon0_target)
    R_NEF[1,0] = -np.sin(lat0_target)*np.sin(lon0_target)
    R_NEF[1,1] = np.cos(lon0_target)
    R_NEF[1,2] = -np.cos(lat0_target)*np.sin(lon0_target)
    R_NEF[2,0] = np.cos(lat0_target)
    R_NEF[2,1] = 0
    R_NEF[2,2] = -np.sin(lat0_target)

    #ECEF origin
    R_N_origin = a/np.sqrt(1-(e_sqr*(np.sin(lat0_target))**2));
    O_ECEF = np.zeros([3,1])
    O_ECEF[0,0] = (R_N_origin + alt0)*np.cos(lat0_target)*np.cos(lon0_target)
    O_ECEF[1,0] = (R_N_origin + alt0)*np.cos(lat0_target)*np.sin(lon0_target)
    O_ECEF[2,0] = ((1-e_sqr)*R_N_origin + alt0)*np.sin(lat0_target)

    #find ECEF X Y Z and offset by the origin
    P_ECEF = R_NEF @ np.array([[N],[E],[D]]) +  O_ECEF;
    
    #convert P_ECEF to LLA (use closed form solution)
    X = P_ECEF[0][0];
    Y = P_ECEF[1][0];
    Z = P_ECEF[2][0];
    LLA_longitude = np.arctan2(Y,X);
    p = np.sqrt(X**2+Y**2);
    theta = np.arctan((Z*a)/(p*b));
    LLA_latitude = np.arctan((Z+e2_sqr*b*(np.sin(theta))**3)/(p-e_sqr*a*(np.cos(theta))**3));
    R_N_LLAlat = a/np.sqrt(1-(e_sqr*(np.sin(LLA_latitude))**2));
    LLA_altitude = p/np.cos(LLA_latitude) - R_N_LLAlat;
    
    #return LLA latitude, longitude and altitude
    P_LLA = (LLA_latitude, LLA_longitude, LLA_altitude);    
    
    return P_LLA

# if __name__ == '__main__':
    
#     lat0_target = d2r(43.67458)
#     lon0_target = d2r(-79.66346)
#     alt0 = 117
#     N = 100
#     E = 150
#     D = 0
    
#     P_LLA = ned2lla(N, E, D, lat0_target, lon0_target, alt0)
    
    
    