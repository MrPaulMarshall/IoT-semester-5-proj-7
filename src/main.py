import tkinter as tk
import threading as th
from conf_loader import load_configuration
from configuration import Configuration
from node_draw import draw_configuration


def start_ui(configuration: Configuration):
    root = tk.Tk()
    root.title('Multi-agent communication in IOT')
    vbar = tk.Scrollbar(root, orient=tk.VERTICAL)
    vbar.pack(side=tk.RIGHT, fill=tk.Y)
    hbar = tk.Scrollbar(root, orient=tk.HORIZONTAL)
    hbar.pack(side=tk.BOTTOM, fill=tk.X)
    canvas = tk.Canvas(root, bg='lightgrey', width=1000, height=1000, yscrollcommand=vbar.set, xscrollcommand=hbar.set,
                       confine=False, scrollregion=(-500, -500, 1000, 1000))
    canvas.pack(expand=tk.YES, fill=tk.BOTH)
    vbar.config(command=canvas.yview)
    hbar.config(command=canvas.xview)
    draw_configuration(configuration, canvas)
    root.mainloop()


def start_app():
    configuration = load_configuration("conf2.json")
    for _, device in configuration.devices.items():
        print(device,  " parent: [", device.masterDevice , "] children = " , device.childrenDevices, " neighbours: ", device.neighbourDevices)
    ui_thread = th.Thread(target=start_ui, args=(configuration,), daemon=True)
    ui_thread.start()

    cameras = [configuration.devices[25], configuration.devices[26]]

    print("--------SIMULATION--------")

    # main simulation loop
    for i in range(100):
        for _, device in configuration.devices.items():
            device.compute()
        if i % 10 == 0:
            for camera in cameras:
                camera.sendFromCamera(camera.createTask(i), camera.masterDevice)

    ui_thread.join()


start_app()
