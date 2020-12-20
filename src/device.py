from random import randint
from time import sleep
from task import Task

class Device:
    # jezeli device to kamera, to computingPower == 0, oraz connectedDevices == tasks == []
    # masterDevice:
    #   kamera -> dzielnica
    #   dzielnica -> miasto
    #   miasto -> cloud

    def __init__(self, deviceID, computingPower):
        self.deviceID = deviceID
        self.maxComputingPower = computingPower
        self.currentComputingPower = computingPower
        self.tasks = []
        self.masterDevice = None
        self.neighbourDevices = []
        self.childrenDevices = []

    def compute(self):
        # TODO
        pass

    def createTask(self):
        # TODO
        pass

    def receiveTask(self):
        # TODO
        pass

    def receiveResults(self, task):
        # TODO
        pass

    def divideTask(self):
        # TODO
        pass

    def sendTask(self):
        # TODO
        pass

    def sendResults(self, results):
        # TODO
        pass

