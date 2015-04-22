import sys
import time
import random
import math
import motion
import almath as m # python's wrapping of almath
import Image

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
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
    'The posture chosen is Stand'
    
    def __init__(self):
        self.name = "Init"
       
    def run(self, robotIP):
        try:
            postureProxy = ALProxy("ALRobotPosture", robotIP, 9559)
        except Exception, e:
            print "Could not create proxy to ALRobotPosture"
            print "Error was: ", e
               
        postureProxy.goToPosture("Stand", 0.8)
        
class stopRobot(Features):
    'Common base class for stopRobot feature'
    'The goal of this feature is to set a posture for the robot'
    'The posture chosen is LyingBack'
    
    def __init__(self):
        self.name = "Stop"
       
    def run(self, robotIP):
        try:
            postureProxy = ALProxy("ALRobotPosture", robotIP, 9559)
        except Exception, e:
            print "Could not create proxy to ALRobotPosture"
            print "Error was: ", e
               
        postureProxy.goToPosture("LyingBack", 0.7)
        
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
            
        try:
            navigationProxy = ALProxy("ALNavigation", robotIP, 9559)
        except Exception, e:
            print "Could not create proxy to ALRobotNavigation"
            print "Error was: ", e
        
        try:
            memoryProxy = ALProxy("ALMemory", robotIP, 9559)
        except Exception, e:
            print "Could not create proxy to ALMemory"
            print "Error was: ", e
        
        try:
            tts = ALProxy("ALTextToSpeech", robotIP, 9559)
        except Exception, e:
            print "Could not create proxy to ALTextToSpeech"
            print "Error was: ", e    
 
        # Send NAO to Pose Init
        postureProxy.goToPosture("StandInit", 0.5)
        
        # setting the language for Nao
        tts.setLanguage("English")
        
        #####################
        ## Enable arms control by Walk algorithm
        #####################
        motionProxy.setWalkArmsEnabled(True, True)
        #~ motionProxy.setWalkArmsEnabled(False, False)
    
        #####################
        ## FOOT CONTACT PROTECTION
        #####################
        motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])
        
        start = time.time()

        while time.time() - start < 30:
            navigationProxy.moveTo(5.0, 0.0, 0.0)
            if memoryProxy.getData("SonarLeftDetected"):
                motionProxy.moveTo(0.0, 0.0, 1.54)
                motionProxy.waitUntilMoveIsFinished()
            elif memoryProxy.getData("SonarRightDetected"):
                motionProxy.moveTo(0.0, 0.0, -1.54)
                motionProxy.waitUntilMoveIsFinished()
    
        'Small message of end'
        tts.say("WAALK FINISHED") #
        print("Walk is over!")
               
class Move(Features):
    'Common base class for Move feature'  
    'The Robot moves in accordance by the parameters given'
    'the parameters are: x,y and theta'
    
    def __init__(self, x, y, theta):
        self.name = "Move"
        self.x = x
        self.y = y
        self.theta = theta  
    
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
        try:
            navigationProxy = ALProxy("ALNavigation", robotIP, 9559)
        except Exception, e:
            print "Could not create proxy to ALRobotNavigation"
            print "Error was: ", e
        
        # Send NAO to Pose Init
        postureProxy.goToPosture("StandInit", 0.6)
    
        navigationProxy.setSecurityDistance(0.5)
        
        X = self.x
        Y = self.y
        Theta = self.theta

        navigationProxy.moveTo(X, Y, Theta)
    
class TakePicture(Features):
    
    def __init__(self):
        self.name = "TakePicture"
    
    def run(self, robotIP):
        try:
            camProxy = ALProxy("ALVideoDevice", robotIP, 9559)
        except Exception, e:
            print "Could not create proxy to ALVideoDevice"
            print "Error was: ", e
            
        resolution = 2  #VGA
        colorSpace = 11 #RGB
        
        videoClient = camProxy.subscribe("python_client", resolution, colorSpace, 5)
        
        t0 = time.time()
            
        # Get a camera image.
        # image[6] contains the image data passed as an array of ASCII chars.
        naoImage = camProxy.getImageRemote(videoClient)
        
        t1 = time.time()
        
        # Time the image transfer.
        print "acquisition delay ", t1 - t0
        
        camProxy.unsubscribe(videoClient)
        
        
        # Now we work with the image returned and save it as a PNG  using ImageDraw package.
        
        # Get the image size and pixel array.
        imageWidth = naoImage[0]
        imageHeight = naoImage[1]
        array = naoImage[6]
        
        # Create a PIL Image from our pixel array.
        im = Image.fromstring("RGB", (imageWidth, imageHeight), array)
        
        # Save the image.
        im.save("camImage.png", "PNG")
        
        im.show()
        
class Mime(Features):
    
    def __init__(self, LShoulderPitch, LShoulderRoll, LElbowYaw, LElbowRoll, RShoulderPitch, RShoulderRoll, RElbowYaw, RElbowRoll):
        self.name = "Mime"
        self.LShoulderPitch = LShoulderPitch
        self.LShoulderRoll = LShoulderRoll
        self.LElbowYaw = LElbowYaw
        self.LElbowRoll = LElbowRoll
        self.RShoulderPitch = RShoulderPitch
        self.RShoulderRoll = RShoulderRoll
        self.RElbowYaw = RElbowYaw
        self.RElbowRoll = RElbowRoll
    
    def run(self, robotIP):
        # Init proxies
        try:
            motionProxy = ALProxy("ALMotion", robotIP, 9559)
        except Exception, e:
            print "Could not create proxy to ALMotion"
            print "Error was: ", e
            sys.exit(1)
        try:
            postureProxy = ALProxy("ALRobotPosture", robotIP, 9559)
        except Exception, e:
            print "Could not create proxy to ALRobotPosture"
            print "Error was: ", e
    
        # Send NAO to Pose Init
        postureProxy.goToPosture("StandInit", 1.0)
        
        #Test example with two joints
        names = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"]
        angleLists = [self.LShoulderPitch, self.LShoulderRoll, self.LElbowYaw, self.LElbowRoll, self.RShoulderPitch, self.RShoulderRoll, self.RElbowYaw, self.RElbowRoll]
        fractionMaxSpeed = 0.3
        
        motionProxy.setAngles(names, angleLists, fractionMaxSpeed)
        
        time.sleep(5.0)
        
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
        
"Testing Features"
#mM = Mime()
#nao = Nao("127.0.0.1",9559)
#mM.runOnRobot(nao)

