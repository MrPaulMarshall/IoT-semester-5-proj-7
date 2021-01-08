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

    def __init__(self, deviceID, computingPower, masterDevice):
        self.deviceID = deviceID
        self.maxComputingPower = computingPower
        self.currentComputingPower = computingPower
        self.masterDevice = masterDevice
        self.neighbourDevices = []
        self.childrenDevices = []

        # slownik {task: przyznanaMocObliczeniowa}
        self.tasksToCompute = {}
        # lista taskow do wyslania gdzie indziej
        self.tasksToSend = []
        # slownik {task: [subtask1, subtask2 ..]}, sluzy do zbierania wynikow z rozeslanych taskow
        self.tasksToJoin = {}

    def __repr__(self):
        return "Id: " + str(self.deviceID)  # + " currentComputingPower: " + str(self.currentComputingPower)

    def compute(self):
        if len(self.tasksToCompute) != 0:
            for task in self.tasksToCompute:
                task.compute(self.tasksToCompute[task])
            finishedTasks = {k: v for k, v in self.tasksToCompute.items() if k.isCompleted()}
            for task in finishedTasks:
                self.currentComputingPower += self.tasksToCompute[task]  # TODO: added line, OK?
                del self.tasksToCompute[task]

                if len(task.divisionHistory) == 0:
                    print(str(task) + ": FINISHED")
                else:
                    result = Result(task)
                    task.sourceDevice.receiveResults(result)

    def createTask(self, i):
        taskID = randint(1, int(1e8))
        computingUnits = randint(10, 200)
        maxTime = randint(1, 10000)
        return Task(taskID, computingUnits, maxTime, self, [i], None)

    def receiveResults(self, result):
        # gdy wynik wroci do kamery
        if len(result.task.divisionHistory) == 1:
            print("Task:", result.task, "returned to camera", self.deviceID)
            return

        parentTask = None
        for task in self.tasksToJoin:
            if result.task.taskID == task.taskID and result.task.divisionHistory[1:] == task.divisionHistory:
                parentTask = task
                break
        self.tasksToJoin[parentTask].append(result.task)
        # jezeli wszystkie subtaski juz sa
        if parentTask.computingUnits <= sum(map(lambda t: t.initialUnits, self.tasksToJoin[parentTask])):
            print(str(parentTask) + ": COLLECTING")
            parentTask.sourceDevice.receiveResults(Result(parentTask))

    def divideTask(self, task, chunkSizes):
        if len(chunkSizes) == 0:
            return None
        subtasks = []
        for idx, size in enumerate(chunkSizes):
            subtask = Task(task.taskID, size, task.maxTime, self, task.divisionHistory, idx)
            subtasks.append(subtask)
        # zwraca liste subtaskow, ktore beda rozsylane do innych urzadzen
        return subtasks

    def sendFromCamera(self, task, dev):
        dev.sendTask(task)

    def sendTask(self, task):
        # gdy sam moze obliczyc
        if self.currentComputingPower > task.computingUnits:
            self.receiveTask(task)
            return
        # rozdziela taski dalej
        else:
            self.tasksToJoin[task] = []

            unitsLeft = task.computingUnits
            chunks = [self.currentComputingPower * 0.6]  # pierwszy subtask dla siebie samego
            unitsLeft -= chunks[0]
            for device in self.neighbourDevices:  # reszta subtaskow dla sasiadow
                tmp = min(unitsLeft, device.currentComputingPower * 0.6)
                chunks.append(tmp)
                unitsLeft -= tmp
                if unitsLeft <= 0:
                    break
            if unitsLeft > 0:  # gdy sasiedzi maja za mala moc, wysyla wyzej
                chunks.append(unitsLeft)

            subtasks = self.divideTask(task, chunks)

            self.receiveTask(subtasks.pop(0))
            for device in self.neighbourDevices:
                device.receiveTask(subtasks.pop(0))
                if not subtasks:
                    break
            if self.masterDevice is not None and subtasks:
                self.masterDevice.sendTask(subtasks.pop(0))
            if self.masterDevice is None and subtasks:
                sub = subtasks.pop(0)
                print('Task:', sub, "SENT TO CLOUD AND RETURNED")
                # returnujemy w dol
                self.receiveResults(Result(sub))

    def receiveTask(self, task):
        # przydziela moc obliczeniowa dla taska TODO: ZMIENIC PRZYZNAWANIE
        if self.currentComputingPower > task.computingUnits:
            self.tasksToCompute[task] = task.computingUnits
            self.currentComputingPower -= task.computingUnits
        else:
            print('WONT HAPPEN')
