import collections

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
        if newIndex != None:
            self.divisionHistory.insert(0, newIndex)

    def __repr__(self):
        return "Id: " + str(self.taskID) + "; Subtask: " + str(self.divisionHistory)

    def compute(self, unitsComputed):
        if self.computingUnits > unitsComputed:
            self.computingUnits -= unitsComputed
        else:
            self.computingUnits = 0
    
    def isCompleted(self):
        if self.computingUnits <= 0:
            return True
        return False

    def __eq__(self, other):
        return self.taskID == other.taskID and self.divisionHistory == other.divisionHistory

    def __hash__(self):
        return self.taskID + sum(self.divisionHistory)
