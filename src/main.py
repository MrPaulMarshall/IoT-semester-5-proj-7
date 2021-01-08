from device import Device
import json

#Funckja przyjmuje ścierzkę do pliku zwraca słownik {"id": obiekt device}
def loadConfiguration(path):
    """
    Funkcja przyjmuje plik JSON. Zwraca słownik z konfiguracją urządzeń.\n
    Paramatry:
    path (string): ścieżka do pliku JSON\n
    Zwraca: słownik {"id", Device}
    """
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
    


devices = loadConfiguration("configurations/conf4.json")
for id in devices:
    print(devices[id],  " parent: [", devices[id].masterDevice , "] children = " , devices[id].childrenDevices, " neighbours: ", devices[id].neighbourDevices)


cameras = []
for id in devices:
    
    if devices[id].maxComputingPower == 0:
        cameras.append(devices[id])

print("--------SIMULATION--------")

# main simulation loop
for i in range(100):
    for id in devices:
        devices[id].compute()
    if i % 10 == 0:
        for camera in cameras:
            camera.sendFromCamera(camera.createTask(i), camera.masterDevice)