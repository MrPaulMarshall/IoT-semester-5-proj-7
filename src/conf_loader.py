import json
from device import Device
from cloud import Cloud
from cityNode import CityNode
from districtNode import DistrictNode
from configuration import Configuration


def load_districts_components(data, parent, devices):
    districtsComponents= []
    for dc in data:
        districtsComponent = []
        for dn in dc['districtsNodes']:
            newDevice = Device(dn['deviceID'], dn['computingPower'], parent)
            devices[dn['deviceID']] = newDevice
            districtNode = DistrictNode(newDevice)
            districtsComponent.append(districtNode)
        for dn in dc['districtsNodes']:
            for neighbourID in dn['neighbours']:
                devices[dn['deviceID']].neighbourDevices.append(devices[neighbourID])
        districtsComponents.append(districtsComponent)
    return districtsComponents


def load_cities_components(data, parent, devices):
    citiesComponents = []
    for cc in data:
        citiesComponent = []
        for cn in cc['citiesNodes']:
            newDevice = Device(cn['deviceID'], cn['computingPower'], parent)
            devices[cn['deviceID']] = newDevice
            cityNode = CityNode(newDevice)
            cityNode.districtsComponents = load_districts_components(cn['districtsComponents'], newDevice, devices)
            citiesComponent.append(cityNode)
        for cn in cc['citiesNodes']:
            for neighbourID in cn['neighbours']:
                devices[cn['deviceID']].neighbourDevices.append(devices[neighbourID])
        citiesComponents.append(citiesComponent)
    return citiesComponents


def load_configuration(file: str, devices):
    with open(file) as confFile:
        data = json.load(confFile)
        configuration = Configuration()
        cloudData = data['cloud']
        if cloudData is not None:
            newDevice = Device(cloudData['deviceID'], cloudData['computingPower'], None)
            devices[cloudData['deviceID']] = newDevice
            cloud = Cloud(newDevice)
            cloud.citiesComponents = load_cities_components(cloudData['citiesComponents'], newDevice, devices)
            cloud.districtsComponents = load_districts_components(cloudData['districtsComponents'], newDevice, devices)
            configuration.cloud = cloud

        districtsData = data['districtsComponents']
        if districtsData is not None:
            configuration.districtsComponents = load_districts_components(districtsData, None, devices)

        citiesData = data['citiesComponents']
        if citiesData is not None:
            configuration.citiesComponents = load_cities_components(citiesData, None, devices)
        return configuration