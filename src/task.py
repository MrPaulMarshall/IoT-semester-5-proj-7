class Task:
    # computingUnits - ilosc jednostek procesora potrzebnych do wykonania obliczenia
    # maxTime - maksymalna ilosc jednostek czasu na wykonanie
    # sourceDevice - urzadzenie ktore przyslalo to zadanie / kawalek
    # divisionHistory - [0, 1, 3, 0] etc.
    #       na i-tym poziome dzielimy task na n kawalkow, o indeksach [0..n-1], i dopisujemy te indeksy do list w kazdym nowym kawalku
    def __init__(self, taskID, computingUnits, maxTime, sourceDevice, divisionHistory, newIndex):
        self.taskID = taskID
        self.computingUnits = computingUnits
        self.maxTime = maxTime
        self.sourceDevice = sourceDevice
        self.divisionHistory = divisionHistory
        self.divisionHistory.insert(0, newIndex)

    def mockupPrint(self):
        print(str(self.taskID) + ': ' + str(self.divisionHistory))

    def compute(self, unitsComputed):
        self.computingUnits -= unitsComputed
        return self.isCompleted()

    def isCompleted(self):
        if self.computingUnits <= 0:
            return True
        return False
