import math

# latitude is phi and longitude is theta relative to earth's center

# converts spherical coordinates (lat & long) to cartesian, then uses distance formula
# margin of error is +- .1 meters
def calcDistance(coords1, coords2): # find distance between two coords
    rho1 = coords1[2] + 6378100
    phi1 = coords1[0]
    theta1 = coords1[1]

    # cos & sin are swapped for cosphi/sinphi
    x1 = rho1*math.cos(phi1*math.pi/180)*math.cos(theta1*math.pi/180) # slightly off from typical conversion; idk why but it works
    y1 = rho1*math.cos(phi1*math.pi/180)*math.sin(theta1*math.pi/180) # slightly off from typical conversion; idk why but it works
    z1 = rho1*math.sin(phi1*math.pi/180) #

    rho2 = coords2[2] + 6378100
    phi2 = coords2[0]
    theta2 = coords2[1]

    #same deal as above
    x2 = rho2*math.cos(phi2*math.pi/180)*math.cos(theta2*math.pi/180)
    y2 = rho2*math.cos(phi2*math.pi/180)*math.sin(theta2*math.pi/180)
    z2 = rho2*math.sin(phi2*math.pi/180)
    return math.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2) # cartesian distance calculated

