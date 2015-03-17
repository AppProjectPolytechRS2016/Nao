import sys

from naoqi import ALProxy
from Features import *
from Nao import *
from NaoApplication import *

class standInit(Features):
    'Common base class for initRobot feature'
    'The goal of this feature is to set a posture for the robot'
    'The posture chosen is SitRelax'
    
    def __init__(self):
       
       self.name = "standInit"
       
       try:
              postureProxy = ALProxy("ALRobotPosture", "127.0.0.1", 9559)
       except Exception, e:
               print "Could not create proxy to ALRobotPosture"
               print "Error was: ", e
               
       postureProxy.goToPosture("Stand", 1.0)

    def runFeatureOnRobot(self, Nao):
           NaoApplication.runFeatureOnRobot(standInit, Nao)
