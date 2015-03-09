import sys

from naoqi import ALProxy

class Nao:
    'Common base class for all Nao'
    
    def __init__(self):
        
        self.NaoPort = 9559
        self.RobotIP = "127.0.0.1"
    
    def getFeature(self):
        'This method will execute the feature called'
        
        
    def standInit(self):

        try:
            postureProxy = ALProxy("ALRobotPosture", self.RobotIP, self.NaoPort)
        except Exception, e:
            print "Could not create proxy to ALRobotPosture"
            print "Error was: ", e
    
        postureProxy.goToPosture("StandInit", 1.0)
           
   
        
    
    
    
    
    