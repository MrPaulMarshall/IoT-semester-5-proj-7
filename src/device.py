from random import randint
from time import sleep
from task import Task
from result import Result

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

        # slownik {task: przyznanaMocObliczeniowa}
        self.tasksToCompute = {}
        # lista taskow do wyslania gdzie indziej
        self.tasksToSend = []
        # slownik {task: [subtask1, subtask2 ..]}, sluzy do zbierania wynikow z rozeslanych taskow
        self.tasksToJoin = {}

    def __repr__(self):
        return "Id: " + str(self.deviceID) #+ " currentComputingPower: " + str(self.currentComputingPower)

    def compute(self):
        if len(self.tasksToCompute) != 0:
            for task in self.tasksToCompute:
                task.compute(self.tasksToCompute[task])
            finishedTasks = {k: v for k, v in self.tasksToCompute.items() if k.isCompleted()}
            for task in finishedTasks:
                del self.tasksToCompute[task]

                if len(task.divisionHistory) == 0:
                    print(str(task) + ": FINISHED")
                else:
                    result = Result(task)
                    task.sourceDevice.receiveResults(result)

    def createTask(self):
        taskID = randint(1, int(1e8))
        computingUnits = randint(1, 100)
        maxTime = randint(1, 1000)
        return Task(taskID, computingUnits, maxTime, self, [], None)

    def receiveResults(self, result):
        parentTask = None
        for task in self.tasksToJoin:
            if result.task.taskID == task.taskID and result.task.divisionHistory[1:] == task.divisionHistory:
                parentTask = task
                break
        self.tasksToJoin[parentTask].append(result)
        # TODO - jezeli wszystkie subtaski juz sa

    def divideTask(self, task, chunkSizes):
        if len(chunkSizes) == 0:
            return None
        subtasks = []
        for idx, size in enumerate(chunkSizes):
            subtask = Task(task.taskID, size, task.maxTime, self, task.divisionHistory, idx)
            subtasks.append(subtask)
        # zwraca liste subtaskow, ktore beda rozslane do innych urzadzen
        return subtasks

    def sendTask(self, task):
        # TODO
        pass

    def receiveTask(self):
        # TODO
        pass
