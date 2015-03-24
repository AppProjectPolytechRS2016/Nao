from FeaturesComplete import *
from Robot import *

class NaoApplication:

    def __init__(self):
          
        self.features = []
        self.robots = []
   
def main():
    
    'Initialization of a new NaoApplication instance'         
    na = NaoApplication()
    
    'Initialization of a new robot Nao'  
    nao = Nao("127.0.0.1",9559)
    print nao
    
    'Initialization of the different features'  
    iR = initRobot()
    sR = stopRobot()
    wA = Walk()
    mR = Move(0,0,0) # Only working if the robot is standing !
    
    'Adding the features to the list of features of the NaoAppliaction instance'
    na.features.append(iR)
    na.features.append(sR)
    na.features.append(wA)
    na.features.append(mR)
    
    'Adding the robot to the list of robots of the NaoApplication instance'
    na.robots.append(nao)
    
    'Tests running different features on a specified robot'         
    #iR.runOnRobot(nao)
    #sR.runOnRobot(nao)
    #wA.runOnRobot(nao)
    #mR.runOnRobot(nao)
       
if __name__ == "__main__":
    main()
     
