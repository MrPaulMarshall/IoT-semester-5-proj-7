from random import randint
from task import Task

from node_draw import Drafter
from node_draw import change_node_color
from node_draw import change_edge_on_push
from node_draw import change_edge_on_pull
from node_draw import change_node_on_push
from node_draw import calculateColor


class Device:
    # jezeli device to kamera, to computingPower == 0, oraz connectedDevices == tasks == []
    # masterDevice:
    #   kamera -> dzielnica
    #   dzielnica -> miasto
    #   miasto -> cloud

    def __init__(self, deviceID, computingPower, masterDevice):
        """Tworzy nowe urządzenie\n
        Parametry: 
        deviceID (string): Unikalne ID urządzenie\n
        computingPower (int): Moc obliczeniowa urządzenia
        """
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
        """Wykonuje zadania przypisane do urządzenia\n
        Po wykonaniu części zadania przesyła wynik do urządzenia od którego zadanie otrzymała\n
        Po wykonaniu całości zadania wypisuje stosowny komunikat
        """
        drafter = Drafter.get_instance(None)

        if len(self.tasksToCompute) != 0:
            for task in self.tasksToCompute:
                task.compute(self.tasksToCompute[task])
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

        #zmien kolor node'a na aktualnie zajmowana moc obliczeniowa
        change_node_color(calculateColor(self.currentComputingPower / self.maxComputingPower), self.deviceID, drafter.canvas, drafter.configuration)



    def createTask(self, i):
        """
        Tworzy nowe losowe zadanie oraz przypisuje je do urządzenia\n
        Parametry: 
        i (int): Mówi o historii dzielenia zadania\n
        Zwraca:
        Task: Stworzone zadanie
        """
        taskID = randint(1, int(1e8))
        computingUnits = randint(50, 200)
        maxTime = randint(1, 10)
        return Task(taskID, computingUnits, maxTime, self, [i], None)

    def receiveResults(self, result):
        """
        Funkcja która przyjmuje rezultat wykonanego zadania \n
        Jeśli zadanie zostało zwrócone do urządzenia w którym zostało utworzone wypisze się stosowny komunikat\n
        Funcja łączy też zakończone podzadania\n
        Parametry: 
        result (result): Rezultat wykonanego zadania

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



    def divideTask(self, task, chunkSizes):
        """Dzieli zadanie na podzadania\n
        Parametry: 
        task (Task): zadanie do podzielenia\n
        chunkSizes (List): Tablica liczb sumujących się do mocy potrzebnej na wykonanie całego zadania\n
        Zwraca:
        List: tablica podzielonych podzadań
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
        """Funkcja dzieli i przydziela zadanie do urządzeń sąsiadujących. Gdy urządzenie jest w stanie samo wykonać zadanie nie przydziela go\n
        Parametry: 
        task (Task): Zadanie do wykonania
        """
        # gdy sam moze obliczyc
        if self.currentComputingPower > task.computingUnits/task.maxTime:
            self.receiveTask(task)
            return
        # rozdziela taski dalej
        else:
            self.tasksToJoin[task] = []

            unitsLeft = task.computingUnits/task.maxTime
            chunks = [self.currentComputingPower * 0.8]  # pierwszy subtask dla siebie samego
            unitsLeft -= chunks[0]
            for device in self.neighbourDevices:  # reszta subtaskow dla sasiadow
                tmp = min(unitsLeft, device.currentComputingPower * 0.8)
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
                print('Task:', sub, "CLOUD RUN OUT OF SPACE")
                # returnujemy w dol
                self.receiveResults(sub)

    def receiveTask(self, task):
        """Funkcja przypisuje zadanie do urządzenia.\n
        Parametry: 
        task (Task): Zadanie do wykonania
        """
        # przydziela moc obliczeniowa dla taska
        if self.currentComputingPower > task.computingUnits/task.maxTime:
            self.tasksToCompute[task] = task.computingUnits/task.maxTime
            self.currentComputingPower -= task.computingUnits/task.maxTime
        else:
            print('WONT HAPPEN')
