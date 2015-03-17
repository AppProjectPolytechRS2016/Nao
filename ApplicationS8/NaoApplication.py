import sys

from Nao import *
from Features import *
from Robot import *
from initRobot import *
from standInit import *

class NaoApplication:

    def __init__(self):
          
        self.features = []
        self.robots = []
   
    def runFeatureOnRobot(self, feature, robot):
        try:
            feature.runFeatureOnRobot(robot)
        except Exception, e:
            print "Error was: ", e
   
    def main(self):
                 
        na = NaoApplication()
          
        iR = initRobot()
        # sI = standInit()
        na.features.append(iR)
        # na.features.append(sI)
          
        nao = Nao()
        na.robots.append(nao)
                 
        na.runFeatureOnRobot(iR.initR(), nao)
        # na.runFeatureOnRobot(sI, nao)
       
if __name__ == "__main__":
       NaoApplication().main()
     
