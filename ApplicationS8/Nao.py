from naoqi import ALProxy

class Nao(object):
    'Common base class for all Nao'
    
    def __init__(self):
        
        self.NaoPort = 9559
        self.RobotIP = "127.0.0.1"
    
    def standInit(self):

        try:
            postureProxy = ALProxy("ALRobotPosture", self.RobotIP, self.NaoPort)
        except Exception, e:
            print "Could not create proxy to ALRobotPosture"
            print "Error was: ", e
    
        postureProxy.goToPosture("StandInit", 1.0)
           
   
        
    
    
    
    
    