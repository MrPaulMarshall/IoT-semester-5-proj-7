from device import Device
from conf_loader import *


devices = {}
load_configuration("conf2.json", devices)
for id in devices:
    print(devices[id],  " parent: [", devices[id].masterDevice , "] children = " , devices[id].childrenDevices, " neighbours: ", devices[id].neighbourDevices)


cameras = [devices[25], devices[26]]

print("--------SIMULATION--------")

# main simulation loop
for i in range(100):
    for id in devices:
        devices[id].compute()
    if i % 10 == 0:
        for camera in cameras:
            camera.sendFromCamera(camera.createTask(i), camera.masterDevice)