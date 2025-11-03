import math

LED_COUNT = 10

class SequenceAlgorithm(object):
    
    def __init__(self):
        self.steps = 9
        self.triggers = 2
        self.sequence = []
        self.active_step = 0

    def update(self):
        '''
        Generates a "Euclidian rhythm" where triggers are
        evenly distributed over a given number of steps.
        Takes in a number of triggers and steps, 
        returns a list of Booleans.
        Based on Jeff Holtzkener's Javascript implementation at
        https://medium.com/code-music-noise/euclidean-rhythms-391d879494df
        '''
        if self.triggers == 0:
            self.sequence = [False] * self.steps
        else:
            slope = self.triggers / self.steps
            result = []
            previous = None
            for i in range(self.steps):
                # adding 0.0001 to correct for imprecise math in CircuitPython.
                current = math.floor((i * slope) + 0.001) 
                result.append(current != previous)
                previous = current
            self.sequence = result
        return self 

    def addStep(self):
        if self.steps < LED_COUNT:
            self.steps += 1
        else:
            self.steps = 1
            self.triggers = 0
            self.active_step = 0
        self.update()
    
    def addTrigger(self):
        if self.triggers < self.steps:
            self.triggers += 1
        else:
            self.triggers = 0
        self.update()

    def incrementActiveStep(self):
        self.active_step = (self.active_step + 1) % self.steps

    def activeStepIsTrigger(self):
        return self.sequence[self.active_step]
        
