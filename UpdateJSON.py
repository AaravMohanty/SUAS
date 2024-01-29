import json

#open current json mission
#take chords in from geo tag
#change current json of current mission

def waypointcreate():
    longitude = int(input("longitude"))
    latitude = int(input("latitude"))
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

with open('WaypointMisson.plan', 'r') as file:
    data = json.load(file)
    data["mission"]["items"].append(waypointcreate())
    newData = json.dumps(data, indent=4)

with open('newWaypointMisson.plan','w') as file:
    file.write(newData)
