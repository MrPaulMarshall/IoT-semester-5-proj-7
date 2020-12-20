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
        self.masterDevice = None
        self.neighbourDevices = []
        self.childrenDevices = []
        self.tasks = []
        self.currentTaskIndex = 0

    def __repr__(self):
        return "Id: " + str(self.deviceID) #+ " currentComputingPower: " + str(self.currentComputingPower)

    def compute(self):
        # receive tasks

        # compute tasks
        if len(self.tasks) != 0:
            pass

        # send results

    def createTask(self):
        taskID = randint(1, int(1e8))
        computingUnits = randint(1, 100)
        maxTime = randint(1, 1000)
        return Task(taskID, computingUnits, maxTime, self, [], None)

    def receiveTask(self):
        # TODO
        pass

    def receiveResults(self, task):
        # TODO
        pass

    def divideTask(self, task, chunkSizes):
        if len(chunkSizes) == 0:
            return None
        subtasks = []
        for idx, size in enumerate(chunkSizes):
            subtask = Task(task.taskID, size, task.maxTime, self, task.divisionHistory, idx)
            subtasks.append(subtask)
        return subtasks

    def sendTask(self):
        # TODO
        pass

    def sendResults(self, results):
        # TODO
        pass

