import tkinter as tk
import threading as th
import time

from conf_loader import load_configuration
from configuration import Configuration
from node_draw import draw_configuration
from node_draw import Drafter
from node_draw import reset_colors


def start_app():
    configuration = load_configuration("conf2.json")
    for _, device in configuration.devices.items():
        print(device,  " parent: [", device.masterDevice , "] children = " , device.childrenDevices, " neighbours: ", device.neighbourDevices)

    drafter = Drafter.get_instance(configuration)

    cameras = configuration.cameras

    print("--------SIMULATION--------")

    # main simulation loop
    for i in range(1000):
        reset_colors(drafter.canvas, configuration)
        for _, device in configuration.devices.items():
            device.compute()
        if i % 10 == 0:
            for camera in cameras:
                camera.sendFromCamera(camera.createTask(i), camera.masterDevice)
        time.sleep(0.25)
        drafter.root.update()

    drafter.root.mainloop()

start_app()
