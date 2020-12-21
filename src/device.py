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
                self.currentComputingPower += self.tasksToCompute[task]  # TODO: added line, need review
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
        # TODO jezeli wszystkie subtaski juz sa
        if len(self.tasksToJoin[parentTask]) == parentTask.divisionHistory[0]:  # TODO to dziala?
            parentTask.sourceDevice.receiveResults(parentTask)

    def divideTask(self, task, chunkSizes):
        if len(chunkSizes) == 0:
            return None
        subtasks = []
        for idx, size in enumerate(chunkSizes):
            subtask = Task(task.taskID, size, task.maxTime, self, task.divisionHistory, idx)
            subtasks.append(subtask)
        # zwraca liste subtaskow, ktore beda rozslane do innych urzadzen
        return subtasks

    def sendTask(self, task, device):
        # TODO tu zmieniamy divisionHistory taska?
        device.receiveTask(task)
        pass

    def receiveTask(self, task):
        # gdy ma wystarczajaco mocy obliczeniowej na taska to wykonuje go sam
        if self.currentComputingPower >= task.computingUnits:
            self.tasksToCompute[task] = task.computingUnits
            self.currentComputingPower -= task.computingUnits
        else:
            chunkSizes = [10,20,30, 100]  # TODO uzaleznic od zmiennych, length <= self + masterDevice + len(neighbours)
            subtasks = self.divideTask(task, chunkSizes)

            self.tasksToJoin[task] = []  # tworzy klucz ktory oczekuje wszystkich subtaskow
            self.receiveTask(subtasks.pop(0))  # pierwszy subtask dla siebie samego, reszte rozsyla innym

            for device in self.neighbourDevices:  # reszta subtaskow, oprocz ostatniego, dla sasiadow
                self.sendTask(subtasks.pop(0), device)

            if len(subtasks) > 0:
                self.sendTask(subtasks.pop(0), self.masterDevice)  # ostatni subtask (jesli istnieje) dla poziomu wyzej

            if len(subtasks) > 0:
                print("Liczba wygenerowanych subtaskow jest za duza!")

