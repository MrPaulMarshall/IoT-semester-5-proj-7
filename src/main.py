from device import Device
import json

# print("JEBAC PIS")

#Funckja przyjmuje ścierzkę do pliku zwraca słownik {"id": obiekt device}
def loadConfiguration(path):
    allDevices = {}
    with open(path) as json_file:
        data = json.load(json_file)

        for device in data["devices"]:
            allDevices[device["id"]] =  Device(device["id"], device["computingPower"])

        for device in data["devices"]:
            if 'parent' in device:
                allDevices[device["id"]].masterDevice = allDevices[device["parent"]]

            if 'children' in device:

                for childrenId in device["children"]:
                    allDevices[device["id"]].childrenDevices.append(allDevices[childrenId])

            if 'neighbours' in device:
                for neighbourId in device["neighbours"]:
                    allDevices[device["id"]].neighbourDevices.append(allDevices[neighbourId])
            
    return allDevices
    


devices = loadConfiguration("conf.json")
for id in devices:
    print(devices[id],  " parent: [", devices[id].masterDevice , "] children = " , devices[id].childrenDevices, " neighbours: ", devices[id].neighbourDevices)
    