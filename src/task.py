import collections

class Task:
    # computingUnits - ilosc jednostek procesora potrzebnych do wykonania obliczenia
    # maxTime - maksymalna ilosc jednostek czasu na wykonanie
    # sourceDevice - urzadzenie ktore przyslalo to zadanie / kawalek
    # divisionHistory - [0, 1, 3, 0] etc.
    #       na i-tym poziome dzielimy task na n kawalkow, o indeksach [0..n-1], i dopisujemy te indeksy do list w kazdym nowym kawalku
    def __init__(self, taskID, computingUnits, maxTime, sourceDevice, divisionHistory, newIndex):
        """Tworzy nowe zadanie\n
        Parametry:
        taskID (Number): Unikalne ID zadania\n
        computingUnits (Number): Ilość jednostek procesora potrzebnych do wykonania obliczenia\n
        maxTime (Number): Maksymalna ilosc jednostek czasu na wykonanie\n
        sourceDevice (Device): Urzadzenie ktore przyslalo to zadanie / kawalek\n
        divisionHistory (List): Lista mówiąca o historii dzielenia pierwotnego zadania\n
        newIndex (Number): Liczba mówiąca o numerze podzadania
        """
        # print(divisionHistory, newIndex)
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
        Funkcja liczy zadanie\n
        Parametry: 
        unitsComputed (Number): Moc poświęcona przez urządzenie na zadanie
        """
        if self.computingUnits > unitsComputed:
            self.computingUnits -= unitsComputed
        else:
            self.computingUnits = 0
    
    def isCompleted(self):
        """Funkcja mówiąca czy zadanie zostało wykonane\n
        Zwraca bool: Podaje informacje o zakończeniu wykonaniu zadania
        """
        
        if self.computingUnits <= 0:
            return True
        return False

    def __eq__(self, other):
        return self.taskID == other.taskID and self.divisionHistory == other.divisionHistory

    def __hash__(self):
        return self.taskID + sum(self.divisionHistory)
