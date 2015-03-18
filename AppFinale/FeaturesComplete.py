import sys
import time
import random

from naoqi import ALProxy
from Robot import *
# from NaoApplication import *

class Features:
    def __init__(self, name):
        self.name = name
    
    def runOnRobot(self, Nao):
        self.run()
              
class initRobot(Features):
    'Common base class for initRobot feature'
    'The goal of this feature is to set a posture for the robot'
    'The posture chosen is StandZero'
    
    def __init__(self):
        self.name = "initRobot"
       
    def run(self):
        try:
            postureProxy = ALProxy("ALRobotPosture", "127.0.0.1", 9559)
        except Exception, e:
            print "Could not create proxy to ALRobotPosture"
            print "Error was: ", e
               
        postureProxy.goToPosture("StandZero", 1.0)
        
class stopRobot(Features):
    'Common base class for stopRobot feature'
    'The goal of this feature is to set a posture for the robot'
    'The posture chosen is SitRelax'
    
    def __init__(self):
        self.name = "stopRobot"
       
    def run(self):
        try:
            postureProxy = ALProxy("ALRobotPosture", "127.0.0.1", 9559)
        except Exception, e:
            print "Could not create proxy to ALRobotPosture"
            print "Error was: ", e
               
        postureProxy.goToPosture("SitRelax", 1.0)
        
class Walk(Features):
    'Common base class for Walk feature'  
    'The Robot whistles while walking and he avoids obstacles'
    
    def __init__(self):
        self.name = "Walk"
    
    def run(self):
        try:
            motionProxy = ALProxy("ALMotion", "127.0.0.1", 9559)
        except Exception, e:
            print "Could not create proxy to ALMotion"
            print "Error was: ", e   
        
        motionProxy.moveInit()
        
        testTime = 10 # seconds
        t = 0
        dt = 0.2
        while (t<testTime):
    
            # WALK
            X         = random.uniform(0.4, 1.0)
            Y         = random.uniform(-0.4, 0.4)
            Theta     = random.uniform(-0.4, 0.4)
            Frequency = random.uniform(0.5, 1.0)
            motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
    
            # JERKY HEAD
            motionProxy.setAngles("HeadYaw", random.uniform(-1.0, 1.0), 0.6)
            motionProxy.setAngles("HeadPitch", random.uniform(-0.5, 0.5), 0.6)
    
            t = t + dt
            time.sleep(dt)
    
        # stop walk on the next double support
        motionProxy.stopMove()
        
        