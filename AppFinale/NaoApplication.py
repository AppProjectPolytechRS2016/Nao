import socket
import json

# IP Jerome : '193.48.125.68' port: 6030
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
    'NAOIP_ORANGE: 193.48.125.63'  
    nao = Nao("193.48.125.63",9559)
    
    'Initialization of the different features'  
    iR = initRobot()
    sR = stopRobot()
    wA = Walk()
    mR = Move(0,0,0)
    # kR = Kick() # NOT FUNCTIONAL
    
    'Adding the features to the list of features of the NaoAppliaction instance'
    na.features.append(iR)
    na.features.append(sR)
    na.features.append(wA)
    na.features.append(mR)
    
    "Getting a list of Features name"
    NaoFeaturesList = []
    for i in range (0, len(na.features)):
        featureName = na.features[i].name
        NaoFeaturesList.append(featureName)
    print ("Liste des fonctionnalites de Nao:")
    print NaoFeaturesList
    
    'Adding the robot to the list of robots of the NaoApplication instance'
    na.robots.append(nao)
    
    'JSON Object Initialization '
    data_ident = {u'From':'193.48.125.67', u'To':'193.48.125.68', u'MsgType':'Ident', u'EquipmentType':'Robot'}
    
    'Serializing Object Data to a JSON formated str'
    result_ident = json.dumps(data_ident)
    
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
    'We are testing here the JSON received to run the right feature'
    while (json.loads(json.dumps(server_msg))["MsgType"]).encode("utf-8") != "End": # We are converting unicode into string in order to compare
        print ("Message received from the server: \n"+server_msg)
        if (json.loads(json.dumps(server_msg))["MsgType"]).encode("utf-8") != "Order":
            if (json.loads(json.dumps(server_msg))["OrderName"]).encode("utf-8") != "Init":
                iR.runOnRobot(nao)
                data_ack = {u'From':'193.48.125.67', u'To':(json.loads(json.dumps(server_msg))["From"]).encode("utf-8"), u'MsgType':'Ack', u'OrderAccepted':True}
                result_ack = json.dumps(data_ack)
                s.send(result_ack+"\r\n")
                server_msg = s.recv(1024)
            elif (json.loads(json.dumps(server_msg))["OrderName"]).encode("utf-8") != "Stop":
                sR.runOnRobot(nao)
                server_msg = s.recv(1024)
            elif (json.loads(json.dumps(server_msg))["OrderName"]).encode("utf-8") != "Move":
                mR.runOnRobot(nao)
                server_msg = s.recv(1024)
            elif (json.loads(json.dumps(server_msg))["OrderName"]).encode("utf-8") != "Walk":
                wA.runOnRobot(nao)
                server_msg = s.recv(1024)
    
    'Tests running different features on a specified robot'         
    #iR.runOnRobot(nao)
    #sR.runOnRobot(nao)
    #wA.runOnRobot(nao)
    #mR.runOnRobot(nao)
    #kR.runOnRobot(nao)  # !!!! WARNING NOT FUNCTIONAL (motion.FRAME_ROBOT is missing)
    
    'Closing the socket'
    s.close()
    print ("The socket has been closed")
    
if __name__ == "__main__":
    main()
     
