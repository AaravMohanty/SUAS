import json

#open current json mission
#take chords in from geo tag
#change current json of current mission

def waypointcreate(longitude, latitude):
    waypoint = {"AMSLAltAboveTerrain": None,
                "Altitude": 75,
                "AltitudeMode": 1,
                "autoContinue": True,
                "command": 22,
                "doJumpId": 6,
                "frame": 3,
                "params": [
                    0,
                    0,
                    0,
                    None,
                    longitude,
                    latitude,
                    100,
                ],
                "type": "SimpleItem"
                }
    return waypoint




if __name__ == "__main__":
    q = [[1, 100, 200, 300, 250], [25, 50, 150, 100, 200]]
    while len(q) != 0:
        temp = q.pop(0)
        coord = [int(temp[1]), int(temp[2]), int(temp[3]), int((temp[4]))] #long, lat, alt, heading
        longitude = coord[0]
        latitude = coord[1] 
        with open('/Users/jeffrey/Documents/QGroundControl/Missions/WaypointMisson.plan', 'r') as file:
            data = json.load(file)
            data["mission"]["items"].append(waypointcreate(longitude, latitude))
            newData = json.dumps(data, indent=4)
        with open('/Users/jeffrey/Documents/QGroundControl/Missions/WaypointMisson.plan','w') as file:
            file.write(newData)
    