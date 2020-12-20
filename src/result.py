class Result:
    def __init__(self, task):
        self.task = task
        # TODO
        self.subresults = []
    
    def join(self, result):
        if result != None:
            self.subresults.insert(result.task.divisionHistory[0], result)
