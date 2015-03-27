import socket
import json

# IP Jerome : '193.48.125.68' port: 6030
from FeaturesComplete import *
from Robot import *

class NaoApplication:

    def __init__(self):
          
        self.features = []
        self.robots = []
        
    def getNaoFeatures(self):
        pass
   
def main():
    
    'Initialization of a new NaoApplication instance'         
    na = NaoApplication()
    
    'Initialization of a new robot Nao'
    'NAOIP_ORANGE: 193.48.125.63'  
    nao = Nao("193.48.125.63",9559)
    
    'Initialization of the different features'  
    iR = initRobot()
    sR = stopRobot()
    wA = Walk()
    mR = Move(0,0,0)
    kR = Kick()
    
    'Adding the features to the list of features of the NaoAppliaction instance'
    na.features.append(iR)
    na.features.append(sR)
    na.features.append(wA)
    na.features.append(mR)
    
    'Printing the List of the features'
    print na.features
    
    'Adding the robot to the list of robots of the NaoApplication instance'
    na.robots.append(nao)
    
    'JSON Object Initialization '
    data_ident = {u'From':'193.48.125.67', u'To':'193.48.125.68', u'MsgType':'Ident', u'EquipmentType':'Robot'}
    
    'Serializing Object Data to a JSON formated str'
    result_ident = json.dumps(data_ident)
    
    print type(json.loads(result_ident)["MsgType"])
    
    'New Socket Initialization'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    'Connection to ComManager'
    s.connect(('193.48.125.68', 6030))
    
    'Sending the Ident Message to the Server'
    s.send(result_ident+"\r\n")
    
    'Printing the Message sent'
    print ("Message sent to the server: \n"+result_ident)
    
    'Receiving Message from the Server'
    server_msg = s.recv(1024)
    
    'Main LOOP of the application'
    while json.loads(json.dumps(s.recv(1024)))["MsgType"] != "End":
        print ("Message received from the server: \n"+server_msg)
        if json.loads(json.dumps(s.recv(1024)))["OrderName"] != "Init":
            iR.runOnRobot(nao)
    
    'Tests running different features on a specified robot'         
    #iR.runOnRobot(nao)
    #sR.runOnRobot(nao)
    #wA.runOnRobot(nao)
    #mR.runOnRobot(nao)
    #kR.runOnRobot(nao)  #!!!! WARNING NOT FUNCTIONAL
    
    'Printing the Message received'
    print ("Message received from the server: \n"+server_msg)
    
    'Closing the socket'
    s.close()
    print ("The socket has been closed")
    
if __name__ == "__main__":
    main()
     
