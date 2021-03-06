import collections

class Task:
    # computingUnits - ilosc jednostek procesora potrzebnych do wykonania obliczenia
    # maxTime - maksymalna ilosc jednostek czasu na wykonanie
    # sourceDevice - urzadzenie ktore przyslalo to zadanie / kawalek
    # divisionHistory - [0, 1, 3, 0] etc.
    #       na i-tym poziome dzielimy task na n kawalkow, o indeksach [0..n-1], i dopisujemy te indeksy do list w kazdym nowym kawalku
    def __init__(self, taskID, computingUnits, maxTime, sourceDevice, divisionHistory, newIndex):
        """Creates new task\n
        Parameters:
        taskID (Number): Unique ID\n
        computingUnits (Number): Computing power needed to compleate task\n
        maxTime (Number): Maximum time needed to compleate the task\n
        sourceDevice (Device): Source device of the task\n
        divisionHistory (List): Lista of numbers. It tells about task division history\n
        newIndex (Number): New index of the task
        """
        self.taskID = taskID
        self.computingUnits = computingUnits

        self.initialUnits = computingUnits

        self.maxTime = maxTime
        self.sourceDevice = sourceDevice
        self.divisionHistory = divisionHistory.copy()
        if newIndex != None:
            self.divisionHistory.insert(0, newIndex)

    def __repr__(self):
        return "Id: " + str(self.taskID) + "; Subtask: " + str(self.divisionHistory)

    def compute(self, unitsComputed):
        """
        Function computes task\n
        Parametars: 
        unitsComputed (Number): Computed units assigned to the task

        Returns amount of computed units
        """
        if self.computingUnits > unitsComputed:
            self.computingUnits -= unitsComputed
            return unitsComputed
        else:
            self.computingUnits = 0
            return 0
    
    def isCompleted(self):
        """It tells if the task is completed\n
        Returns bool: True if compleated False otherwise
        """
        
        if self.computingUnits <= 0:
            return True
        return False

    def __eq__(self, other):
        return self.taskID == other.taskID and self.divisionHistory == other.divisionHistory

    def __hash__(self):
        return self.taskID + sum(self.divisionHistory)
