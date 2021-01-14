from random import randint
from task import Task

from node_draw import Drafter
from node_draw import change_node_color
from node_draw import change_edge_on_push
from node_draw import change_edge_on_pull
from node_draw import change_node_on_push
from node_draw import calculateColor
from node_draw import change_node_on_pull


class Device:
    # jezeli device to kamera, to computingPower == 0, oraz connectedDevices == tasks == []
    # masterDevice:
    #   kamera -> dzielnica
    #   dzielnica -> miasto
    #   miasto -> cloud

    def __init__(self, deviceID, computingPower, masterDevice):
        """Creates new device\n
        Parameters: 
        deviceID (string): Unical ID\n
        computingPower (int): Maximum computing power od the device
        """
        self.deviceID = deviceID
        self.maxComputingPower = computingPower
        self.currentComputingPower = computingPower
        self.masterDevice = masterDevice
        self.neighbourDevices = []
        self.usedPower = 0
        # slownik {task: przyznanaMocObliczeniowa}
        self.tasksToCompute = {}
        # slownik {task: [subtask1, subtask2 ..]}, sluzy do zbierania wynikow z rozeslanych taskow
        self.tasksToJoin = {}

    def __repr__(self):
        return "Id: " + str(self.deviceID)  # + " currentComputingPower: " + str(self.currentComputingPower)

    def compute(self):
        """Performs tasks assign to the device\n
        After completing part of the task it sends the output to the source device\n
        After completeng whole task it prints message
        """
        drafter = Drafter.get_instance(None)

        if len(self.tasksToCompute) != 0:
            for task in self.tasksToCompute:
                self.usedPower += task.compute(self.tasksToCompute[task])

            finishedTasks = {k: v for k, v in self.tasksToCompute.items() if k.isCompleted()}
            for task in finishedTasks:
                self.currentComputingPower += self.tasksToCompute[task]
                del self.tasksToCompute[task]

                if len(task.divisionHistory) == 0:
                    print(str(task) + ": FINISHED")
                else:
                    task.sourceDevice.receiveResults(task)
                    #gdy task wraca zmien kolor na niebieski
                    change_edge_on_pull(self.deviceID, task.sourceDevice.deviceID, drafter.canvas, drafter.configuration)
                    if task.sourceDevice.masterDevice.deviceID is self.deviceID:
                        change_node_on_pull(task.sourceDevice.deviceID, drafter.canvas, drafter.configuration)

        #zmien kolor node'a na aktualnie zajmowana moc obliczeniowa
        change_node_color(calculateColor(self.currentComputingPower / self.maxComputingPower), self.deviceID, drafter.canvas, drafter.configuration)



    def createTask(self, i):
        """
        Creates new random task and assigns it to the device\n
        Parameters: 
        i (int): Tells about the division history of the task\n
        Returns:
        Task: Newly created task
        """
        taskID = randint(1, int(1e8))
        computingUnits = randint(50, 200)
        maxTime = randint(1, 10)
        return Task(taskID, computingUnits, maxTime, self, [i], None)

    def receiveResults(self, result):
        """
        Function that receives resultat of the completed task\n
        If this device is the source device function prints a message\n
        Funcja łączy też zakończone podzadania\n
        Function also joins compleated subtasks\n
        Parameters: 
        result (result): Task result

        """
        # gdy wynik wroci do kamery
        if len(result.divisionHistory) == 1:
            print("Task:", result, "returned to camera", self.deviceID)
            return

        parentTask = None
        for task in self.tasksToJoin:
            if result.taskID == task.taskID and result.divisionHistory[1:] == task.divisionHistory:
                parentTask = task
                break
        self.tasksToJoin[parentTask].append(result)
        # jezeli wszystkie subtaski juz sa
        if parentTask.computingUnits <= sum(map(lambda t: t.initialUnits, self.tasksToJoin[parentTask])):
            print(str(parentTask) + ": COLLECTING")

            parentTask.sourceDevice.receiveResults(parentTask)
            drafter = Drafter.get_instance(None)
            change_edge_on_pull(self.deviceID, parentTask.sourceDevice.deviceID, drafter.canvas,
                              drafter.configuration)
            if parentTask.sourceDevice.masterDevice.deviceID is self.deviceID:
                change_node_on_pull(parentTask.sourceDevice.deviceID, drafter.canvas, drafter.configuration)



    def divideTask(self, task, chunkSizes):
        """Divide task and create subtasks\n
        Parameters: 
        task (Task): task to divide\n
        chunkSizes (List): Tablica liczb sumujących się do mocy potrzebnej na wykonanie całego zadania\n
        chunkSizes (List): Array of numbers. Sum of the list must be equal to Task.computingUnits
        Returns:
        List: array of subtasks
        """
        if len(chunkSizes) == 0:
            return None
        subtasks = []
        for idx, size in enumerate(chunkSizes):
            
            subtask = Task(task.taskID, size*task.maxTime, task.maxTime, self, task.divisionHistory, idx)
            subtasks.append(subtask)
        # zwraca liste subtaskow, ktore beda rozsylane do innych urzadzen
        return subtasks

    def sendFromCamera(self, task, dev):
        dev.sendTask(task)
        drafter = Drafter.get_instance(None)
        change_node_on_push(self.deviceID, drafter.canvas, drafter.configuration)
        change_edge_on_push(self.deviceID, dev.deviceID, drafter.canvas, drafter.configuration)

    def sendTask(self, task):
        """
        Function divides task and assigns the subtasks to the device neighbours (if its nessesary).\n
        Parameters: 
        task (Task): Task to compute
        """
        # gdy sam moze obliczyc
        if self.currentComputingPower > task.computingUnits/task.maxTime:
            self.receiveTask(task)
            return
        # rozdziela taski dalej
        else:
            self.tasksToJoin[task] = []

            unitsLeft = task.computingUnits/task.maxTime
            chunks = [self.currentComputingPower * 0.5]  # pierwszy subtask dla siebie samego
            unitsLeft -= chunks[0]
            for device in self.neighbourDevices:  # reszta subtaskow dla sasiadow
                tmp = min(unitsLeft, device.currentComputingPower * 0.5)
                chunks.append(tmp)
                unitsLeft -= tmp
                if unitsLeft <= 0:
                    break
            if unitsLeft > 0:  # gdy sasiedzi maja za mala moc, wysyla wyzej
                chunks.append(unitsLeft)
            subtasks = self.divideTask(task, chunks)

            drafter = Drafter.get_instance(None)

            self.receiveTask(subtasks.pop(0))
            for device in self.neighbourDevices:
                device.receiveTask(subtasks.pop(0))
                change_edge_on_push(self.deviceID, device.deviceID, drafter.canvas, drafter.configuration)
                if not subtasks:
                    break
            if self.masterDevice is not None and subtasks:
                change_node_on_push(self.deviceID, drafter.canvas, drafter.configuration)
                change_edge_on_push(self.deviceID, self.masterDevice.deviceID, drafter.canvas, drafter.configuration)
                self.masterDevice.sendTask(subtasks.pop(0))
            if self.masterDevice is None and subtasks:
                sub = subtasks.pop(0)
                print('Task:', sub, " - CLOUD RAN OUT OF SPACE")
                # returnujemy w dol
                self.receiveResults(sub)

    def receiveTask(self, task):
        """Function assigns task to the device.\n
        Parameters: 
        task (Task): Task to assign
        """
        # przydziela moc obliczeniowa dla taska
        if self.currentComputingPower > task.computingUnits/task.maxTime:
            self.tasksToCompute[task] = task.computingUnits/task.maxTime
            self.currentComputingPower -= task.computingUnits/task.maxTime
