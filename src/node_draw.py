import tkinter as tk
import math as math
from device import Device
from cityNode import CityNode
from districtNode import DistrictNode
from configuration import Configuration


def change_node_color(color: str, deviceId: int, canvas: tk.Canvas, configuration: Configuration):
    idx = configuration.get_node_idx(deviceId)
    canvas.itemconfig(idx, fill=color)


def change_edge_color(color: str, deviceId1: int, deviceId2: int, canvas: tk.Canvas, configuration: Configuration):
    idx1 = configuration.get_node_idx(deviceId1)
    idx2 = configuration.get_node_idx(deviceId2)
    edge_id = configuration.get_edge_id(idx1, idx2)
    edge_idx = configuration.get_edge_idx(edge_id)
    canvas.itemconfig(edge_idx, fill=color)


def draw_wheel(x: float, y: float, radius: float, color: str, canvas: tk.Canvas) -> int:
    wheel = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)
    return wheel


def draw_circle(x: float, y: float, radius: float, color: str, canvas: tk.Canvas) -> int:
    circle = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, outline=color, width=2)
    return circle


def draw_wheels_in_circle(x: float, y: float, radius: float, num_of_wheels: int, canvas: tk.Canvas) -> []:
    wheels = []
    if num_of_wheels == 1:
        wheel = draw_wheel(x, y, 10, 'green', canvas)
        wheels.append(wheel)
    else:
        for i in range(num_of_wheels):
            gamma = i * (2 * math.pi / num_of_wheels)
            wheel = draw_wheel(x + radius * math.cos(gamma), y + radius * math.sin(gamma), 10, 'green', canvas)
            wheels.append(wheel)
    return wheels


def get_object_coords(obj: int, canvas: tk.Canvas):
    coords = canvas.coords(obj)
    x = (coords[0] + coords[2]) / 2
    y = (coords[1] + coords[3]) / 2
    return x, y


def get_oval_radius(obj: int, canvas: tk.Canvas):
    coords = canvas.coords(obj)
    x_rad = (coords[2] - coords[0]) / 2
    return x_rad


def get_rotation(x1, y1, x2, y2):
    if x2 == x1:
        return math.pi / 2
    else:
        slope = (y2 - y1) / (x2 - x1)
        gamma = math.atan(slope)
        return gamma


def draw_connection(obj1: int, obj2: int, canvas: tk.Canvas):
    if obj1 == obj2:
        return
    x1, y1 = get_object_coords(obj1, canvas)
    x2, y2 = get_object_coords(obj2, canvas)
    gamma = get_rotation(x1, y1, x2, y2)
    sign = 1
    if x2 > x1:
        sign = -1
    x1 -= (get_oval_radius(obj1, canvas) + 5) * math.cos(gamma) * sign
    y1 -= (get_oval_radius(obj1, canvas) + 5) * math.sin(gamma) * sign
    x2 += (get_oval_radius(obj2, canvas) + 5) * math.cos(gamma) * sign
    y2 += (get_oval_radius(obj2, canvas) + 5) * math.sin(gamma) * sign
    line = canvas.create_line(x1, y1, x2, y2, width=2, fill='black')
    return line


def connect_children(deviceId: int, componentIdx: int, children: [], canvas: tk.Canvas, configuration: Configuration):
    deviceIdx = configuration.get_node_idx(deviceId)
    edge_id = configuration.add_connection(deviceIdx, componentIdx)
    if edge_id:
        line = draw_connection(componentIdx, deviceIdx, canvas)
        configuration.add_edge_to_idx(edge_id, line)
        for child in children:
            edge_id = configuration.add_connection(deviceIdx, configuration.get_node_idx(child.device.deviceID))
            if edge_id:
                configuration.add_edge_to_idx(edge_id, line)


def draw_component(x: float, y: float, radius: float, color: str, canvas: tk.Canvas, nodes: [DistrictNode], configuration: Configuration):
    num_of_nodes = len(nodes)
    if num_of_nodes == 1:
        wheel = draw_wheel(x, y, 10, color, canvas)
        configuration.add_node_to_idx(nodes[0].device.deviceID, wheel)
    else:
        for i in range(num_of_nodes):
            gamma = i * (2 * math.pi / num_of_nodes)
            wheel = draw_wheel(x + radius * math.cos(gamma), y + radius * math.sin(gamma), 10, color, canvas)
            configuration.add_node_to_idx(nodes[i].device.deviceID, wheel)
    circle = draw_circle(x, y, radius * 1.5, 'black', canvas)
    for node in nodes:
        for neighbour in node.device.neighbourDevices:
            deviceIdx = configuration.get_node_idx(node.device.deviceID)
            neighbourIdx = configuration.get_node_idx(neighbour.deviceID)
            edge_id = configuration.add_connection(deviceIdx, neighbourIdx)
            if edge_id:
                line = draw_connection(deviceIdx, neighbourIdx, canvas)
                configuration.add_edge_to_idx(edge_id, line)
    return circle


def draw_cities_component(x: float, y: float, radius: float, canvas: tk.Canvas, city_nodes: [CityNode], configuration: Configuration):
    num_of_nodes = 0
    for city_node in city_nodes:
        num_of_nodes += len(city_node.districtsComponents)
    circle = draw_component(x, y, radius, 'blue', canvas, city_nodes, configuration)

    i = 0
    for city_node in city_nodes:
        for district_component in city_node.districtsComponents:
            gamma = i * (2 * math.pi / num_of_nodes)
            component = draw_component(x + radius * 3.2 * math.cos(gamma), y + radius * 3.2 * math.sin(gamma), radius, 'green', canvas, district_component, configuration)
            connect_children(city_node.device.deviceID, component, district_component, canvas, configuration)
            i += 1
    return circle


def draw_configuration(configuration: Configuration, canvas: tk.Canvas):
    is_cloud = True
    if configuration.cloud is None:
        is_cloud = False
    # num_of_cities_components = len(configuration.cloud.citiesComponents)
    # num_of_districts_components = len(configuration.cloud.districtsComponents)
    # print(num_of_cities_components)
    # print(num_of_districts_components)
    x = 500
    y = 500
    wheel = draw_wheel(x, y, 10, 'gold', canvas)
    configuration.add_node_to_idx(configuration.cloud.device.deviceID, wheel)
    i = 0
    radius = 300
    num_of_components = len(configuration.cloud.citiesComponents) + len(configuration.cloud.districtsComponents)
    for cities_component in configuration.cloud.citiesComponents:
        gamma = i * (2 * math.pi / num_of_components)
        component = draw_cities_component(x + radius * 2 * math.cos(gamma), y + radius * 2 * math.sin(gamma), 100, canvas, cities_component, configuration)
        connect_children(configuration.cloud.device.deviceID, component, cities_component, canvas, configuration)
        i += 1
    for districts_component in configuration.cloud.districtsComponents:
        gamma = i * (2 * math.pi / num_of_components)
        component = draw_component(x + radius * math.cos(gamma), y + radius * math.sin(gamma), 100, 'green', canvas, districts_component, configuration)
        connect_children(configuration.cloud.device.deviceID, component, districts_component, canvas, configuration)
        i += 1