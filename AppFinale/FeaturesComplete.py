import sys
import time
import random
import math
import motion
import almath as m # python's wrapping of almath

from naoqi import ALProxy
from Robot import *
from NaoApplication import *

class Features:
    def __init__(self, name):
        self.name = name
    
    def runOnRobot(self, Nao):
        self.run(Nao.NaoIP)
              
class initRobot(Features):
    'Common base class for initRobot feature'
    'The goal of this feature is to set a posture for the robot'
    'The posture chosen is StandZero'
    
    def __init__(self):
        self.name = "initRobot"
       
    def run(self, robotIP):
        try:
            postureProxy = ALProxy("ALRobotPosture", robotIP, 9559)
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
       
    def run(self, robotIP):
        try:
            postureProxy = ALProxy("ALRobotPosture", robotIP, 9559)
        except Exception, e:
            print "Could not create proxy to ALRobotPosture"
            print "Error was: ", e
               
        postureProxy.goToPosture("SitRelax", 1.0)
        
class Walk(Features):
    'Common base class for Walk feature'  
    'The Robot whistles while walking and he avoids obstacles'
    
    def __init__(self):
        self.name = "Walk"
    
    def run(self, robotIP):
        try:
            motionProxy = ALProxy("ALMotion", robotIP, 9559)
        except Exception, e:
            print "Could not create proxy to ALMotion"
            print "Error was: ", e   
        
        try:
            postureProxy = ALProxy("ALRobotPosture", robotIP, 9559)
        except Exception, e:
            print "Could not create proxy to ALRobotPosture"
            print "Error was: ", e
        
        # Send NAO to Pose Init
        postureProxy.goToPosture("StandInit", 1.0)
        
        #####################
        ## Enable arms control by Walk algorithm
        #####################
        motionProxy.setWalkArmsEnabled(True, True)
        #~ motionProxy.setWalkArmsEnabled(False, False)
    
        #####################
        ## FOOT CONTACT PROTECTION
        #####################
        #~ motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", False]])
        motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])
    
        #TARGET VELOCITY
        X = -0.5  #backward
        Y = 0.0
        Theta = 0.0
        Frequency =0.0 # low speed
        motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
    
        time.sleep(4.0)
    
        #TARGET VELOCITY
        X = 0.8
        Y = 0.0
        Theta = 0.0
        Frequency =1.0 # max speed
        motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
    
        time.sleep(4.0)
    
        #TARGET VELOCITY
        X = 0.2
        Y = -0.5
        Theta = 0.2
        Frequency =1.0
        motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
    
        time.sleep(2.0)
    
        #####################
        ## Arms User Motion
        #####################
        # Arms motion from user have always the priority than walk arms motion
        JointNames = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll"]
        Arm1 = [-40,  25, 0, -40]
        Arm1 = [ x * motion.TO_RAD for x in Arm1]
    
        Arm2 = [-40,  50, 0, -80]
        Arm2 = [ x * motion.TO_RAD for x in Arm2]
    
        pFractionMaxSpeed = 0.6
    
        motionProxy.angleInterpolationWithSpeed(JointNames, Arm1, pFractionMaxSpeed)
        motionProxy.angleInterpolationWithSpeed(JointNames, Arm2, pFractionMaxSpeed)
        motionProxy.angleInterpolationWithSpeed(JointNames, Arm1, pFractionMaxSpeed)
    
        time.sleep(2.0)
    
        #####################
        ## End Walk
        #####################
        #TARGET VELOCITY
        X = 0.0
        Y = 0.0
        Theta = 0.0
        motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
        
class Move(Features):
    'Common base class for Move feature'  
    'The Robot moves in accordance by the parameters given'
    'the parameters are: x,y and theta'
    
    def __init__(self, x, y, theta):
        self.name = "Walk"
        self.x = x
        self.y = y
        self.theta = theta  
    
    def run(self, robotIP):
        try:
            motionProxy = ALProxy("ALMotion", robotIP, 9559)
        except Exception, e:
            print "Could not create proxy to ALMotion"
            print "Error was: ", e
    
        #####################
        ## Enable arms control by move algorithm
        #####################
        motionProxy.setWalkArmsEnabled(True, True)
        #~ motionProxy.setWalkArmsEnabled(False, False)
    
        #####################
        ## FOOT CONTACT PROTECTION
        #####################
        #~ motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION",False]])
        motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])
    
        #####################
        ## get robot position before move
        #####################
        initRobotPosition = m.Pose2D(motionProxy.getRobotPosition(False))
    
        X = self.x
        Y = self.y
        Theta = self.theta

        motionProxy.post.moveTo(X, Y, Theta)
        # wait is useful because with post moveTo is not blocking function
        motionProxy.waitUntilMoveIsFinished()
    
        #####################
        ## get robot position after move
        #####################
        endRobotPosition = m.Pose2D(motionProxy.getRobotPosition(False))
    
        #####################
        ## compute and print the robot motion
        #####################
        robotMove = m.pose2DInverse(initRobotPosition)*endRobotPosition
        print "Robot Move :", robotMove

class Kick(Features):
     
     def __init__(self):
        self.name = "Kick"
        
     def run(self, robotIP):
        # Init proxies.
        try:
            proxy = ALProxy("ALMotion", robotIP, 9559)
        except Exception, e:
            print "Could not create proxy to ALMotion"
            print "Error was: ", e
    
        try:
            postureProxy = ALProxy("ALRobotPosture", robotIP, 9559)
        except Exception, e:
            print "Could not create proxy to ALRobotPosture"
            print "Error was: ", e
    
        # Send NAO to Pose Init
        postureProxy.goToPosture("StandInit", 1.0)
    
        # Activate Whole Body Balancer
        isEnabled  = True
        proxy.wbEnable(isEnabled)
    
        # Legs are constrained fixed
        stateName  = "Fixed"
        supportLeg = "Legs"
        proxy.wbFootState(stateName, supportLeg)
    
        # Constraint Balance Motion
        isEnable   = True
        supportLeg = "Legs"
        proxy.wbEnableBalanceConstraint(isEnable, supportLeg)
    
        # Com go to LLeg
        supportLeg = "LLeg"
        duration   = 2.0
        proxy.wbGoToBalance(supportLeg, duration)
    
        # RLeg is free
        stateName  = "Free"
        supportLeg = "RLeg"
        proxy.wbFootState(stateName, supportLeg)
    
        # RLeg is optimized
        effectorName = "RLeg"
        axisMask     = 63
        space        = motion.FRAME_ROBOT
    
    
        # Motion of the RLeg
        dx      = 0.05                 # translation axis X (meters)
        dz      = 0.05                 # translation axis Z (meters)
        dwy     = 5.0*math.pi/180.0    # rotation axis Y (radian)
    
    
        times   = [2.0, 2.7, 4.5]
        isAbsolute = False
    
        targetList = [
          [-dx, 0.0, dz, 0.0, +dwy, 0.0],
          [+dx, 0.0, dz, 0.0, 0.0, 0.0],
          [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
    
        proxy.positionInterpolation(effectorName, space, targetList,
                                     axisMask, times, isAbsolute)
    
    
        # Example showing how to Enable Effector Control as an Optimization
        isActive     = False
        proxy.wbEnableEffectorOptimization(effectorName, isActive)
    
        # Com go to LLeg
        supportLeg = "RLeg"
        duration   = 2.0
        proxy.wbGoToBalance(supportLeg, duration)
    
        # RLeg is free
        stateName  = "Free"
        supportLeg = "LLeg"
        proxy.wbFootState(stateName, supportLeg)
    
        effectorName = "LLeg"
        proxy.positionInterpolation(effectorName, space, targetList,
                                    axisMask, times, isAbsolute)
    
        time.sleep(1.0)
    
        # Deactivate Head tracking
        isEnabled    = False
        proxy.wbEnable(isEnabled)
    
        # send robot to Pose Init
        postureProxy.goToPosture("StandInit", 1.0)
        