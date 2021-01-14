import time

import random
from conf_loader import load_configuration
from node_draw import Drafter
from node_draw import reset_colors

import sys


configPath = "configurations/conf4-4-4.json"
simulationTime = 1000
timeDelay = 0.5
        
for i in range(1,len(sys.argv), 2):
    if sys.argv[i] == "-c" and i+1<len(sys.argv):
        simulationTime = int(sys.argv[i+1])
        print("time",simulationTime)
    elif sys.argv[i] == "-t" and i+1<len(sys.argv):
        timeDelay = float(sys.argv[i+1])
        print("timeDelay",timeDelay)
    elif sys.argv[i] == "-p" and i+1<len(sys.argv):
        configPath = sys.argv[i+1]
        print("configPath",configPath)



def start_app():
    configuration = load_configuration(configPath)
    for _, device in configuration.devices.items():
        print(device,  " parent: [", device.masterDevice ," neighbours: ", device.neighbourDevices)

    
    drafter = Drafter.get_instance(configuration)

    cameras = configuration.cameras
    # for _, device in configuration.devices.items():
    #     print(device.maxComputingPower)
    #     if device.maxComputingPower == 1:
    #         cameras.append(device)

    print("--------SIMULATION--------")

    # main simulation loop


    for i in range(simulationTime):
        reset_colors(drafter.canvas, configuration)

        for _, device in configuration.devices.items():
            device.compute()

        for camera in cameras:
            if random.random() <= configuration.taskChance:
                camera.sendFromCamera(camera.createTask(i), camera.masterDevice)

        time.sleep(timeDelay)
        drafter.root.update()

    print("Simulation ended")

    for _, device in configuration.devices.items():
        if device.maxComputingPower == 1 or device.maxComputingPower == 0:
            continue
        averagePerformance = device.usedPower/simulationTime
        averagePercent = 100*averagePerformance/device.maxComputingPower
        print("Device", device.deviceID, "has performed total of", "%.2f" % device.usedPower, "calculations. On average it performed", "%.2f" % averagePerformance, "calculations per cycle which is", "%.2f" % averagePercent, "% of its maximum capability.")


    # drafter.root.mainloop()





start_app()
