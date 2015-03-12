import sys

from naoqi import ALProxy
from Nao import *
from Features import *
from Robot import *
from initRobot import *

class NaoApplication:

       def __init__(self):
              
              self.features = []
              self.robots = []
       
       def runFeatureOnRobot(self, feature, robot):
              try:
                   feature.runFeatureOnRobot(robot)
              except Exception, e:
                   print "Error was: ", e
       
def main():
              
       na = NaoApplication()
       
       iR = initRobot()
       na.features.append(iR)
       
       nao = Nao()
       na.robots.append(nao)
              
       na.runFeatureOnRobot(iR, nao)
       
if __name__ == "__main__":
       main()
     
