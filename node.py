##--------------------------------------------------------------------\
#   matplotlib wxpython example
#   'node.py'
#   Class for nodes with two different movement models: random, and random walk
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu)
#   February 2, 2023
##--------------------------------------------------------------------\

import random

class Node():
    def __init__(self, randMin, randMax) :
        """
        Args:
            randMin: int
                Minimum bounary walk model can traverse (same for x, y, and z axes)
            randMax: int
                Maximum bounary walk model can traverse (same for x, y and z axes)
        """

        self.currentLoc = (0,0,0)
        self.pastLocs = []
        self.minRange = randMin
        self.maxRange = randMax

    def getCurrentLoc(self):
        """returns tuple of current x,y,z location"""
        return self.currentLoc

    def getPastLocs(self):
        """returns list of tuples for all past x,y,z locations"""
        return self.pastLocs

    def randomLocation(self):
        """Next location based on completely random points"""

        x = random.randrange(self.minRange, self.maxRange)
        y = random.randrange(self.minRange, self.maxRange)
        z = random.randrange(self.minRange, self.maxRange)        

        self.currentLoc = (x,y,z)
        self.pastLocs.append(self.currentLoc)

    def randomWalk(self):
        """Next location based on random walk model
        
            Since the steps are incremented from last location,
            if the node is out of bounds in any direction, that
            axes is set to the closes boundary value        
        """  

        minNum = self.minRange/10
        maxNum = self.maxRange/10
        x = self.currentLoc[0] + random.randrange(minNum, maxNum)
        y = self.currentLoc[1] + random.randrange(minNum, maxNum)
        z = self.currentLoc[2] + random.randrange(minNum, maxNum)

        if x > self.maxRange:
            x = self.maxRange
        elif x < self.minRange:
            x = self.minRange

        if y > self.maxRange:
            y = self.maxRange
        elif y < self.minRange:
            y = self.minRange

        if z > self.maxRange:
            z = self.maxRange
        elif z < self.minRange:
            z = self.minRange
         
        self.currentLoc = (x,y,z)
        self.pastLocs.append(self.currentLoc)   
