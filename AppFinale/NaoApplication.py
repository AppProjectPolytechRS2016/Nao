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
    
    # "Getting the list of available robots"
    #AvailableNao = []
    #for j in range (0, len(na.robots)):
    #    robotName = na.robots[i].name
    #    AvailableNao.append(robotName)
    #print ("List of available robots:")
    #print AvailableNao
    
    'Adding the robot to the list of robots of the NaoApplication instance'
    na.robots.append(nao)
    
    'JSON Object Initialization '
    data_ident = {'From':'193.48.125.67', 'To':'193.48.125.64', 'MsgType':'Ident', 'EquipmentType':'Robot'}
    
    'Serializing Object Data to a JSON formated str'
    result_ident = json.dumps(data_ident)
    
    'New Socket Initialization'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    'Connection to ComManager'
    try:
        s.connect(('193.48.125.68', 6030))
 
    except socket.error:
        print 'Socket connection failed! Host is unreachable! Exiting program'
        s.close()
        sys.exit(0)
   
    
    'Sending the Ident Message to the Server'
    s.send(result_ident+"\r\n")
    
    'Printing the Message sent'
    print ("Message sent to the server: \n"+result_ident)
    
    'Receiving Message from the Server'
    #server_msg = {u'From':'193.48.125.67', u'To':'193.48.125.68', u'MsgType':'Order', u'OrderName':'ConnectTo'}
    server_msg = s.recv(1024).decode("utf-8")
    print type(server_msg)
    print ("Message received from the server: \n"+server_msg)
    
    'Main LOOP of the application'
    'We are testing here the JSON received to run the right feature'
    while (json.loads(server_msg)["MsgType"]).encode("utf-8") != "End":
        if (json.loads(server_msg)["MsgType"]).encode("utf-8") == "Order":
            if (json.loads(server_msg)["OrderName"]).encode("utf-8") == "ConnectTo":
                data_ack = {'From':'193.48.125.67', 'To':(json.loads(server_msg)["From"]).encode("utf-8"), 'MsgType':'Ack', 'OrderAccepted':True, 'FeatureList':NaoFeaturesList}
                result_ack = json.dumps(data_ack)
                s.send(result_ack+"\r\n")
                print ("Message sent to the server: \n"+result_ack)
                #iR.runOnRobot(nao)
                server_msg = s.recv(1024).decode("utf-8")
                print ("Message received from the server: \n"+server_msg)
            elif (json.loads(server_msg)["OrderName"]).encode("utf-8") == "Init":
                #iR.runOnRobot(nao)
                data_ack = {'From':'193.48.125.67', 'To':(json.loads(server_msg)["From"]).encode("utf-8"), 'MsgType':'Ack', 'OrderAccepted':True}
                result_ack = json.dumps(data_ack)
                s.send(result_ack+"\r\n")
                print ("Message sent to the server: \n"+result_ack)
                server_msg = s.recv(1024).decode("utf-8")
                print ("Message received from the server: \n"+server_msg)
            elif (json.loads(server_msg)["OrderName"]).encode("utf-8") == "Stop":
                sR.runOnRobot(nao)
                data_ack = {'From':'193.48.125.67', 'To':(json.loads(server_msg)["From"]).encode("utf-8"), 'MsgType':'Ack', 'OrderAccepted':True}
                result_ack = json.dumps(data_ack)
                s.send(result_ack+"\r\n")
                print ("Message sent to the server: \n"+result_ack)
                server_msg = s.recv(1024).decode("utf-8")
                print ("Message received from the server: \n"+server_msg)
            elif (json.loads(server_msg)["OrderName"]).encode("utf-8") == "Move":
                mR.runOnRobot(nao)
                data_ack = {'From':'193.48.125.67', 'To':(json.loads(server_msg)["From"]).encode("utf-8"), 'MsgType':'Ack', 'OrderAccepted':True}
                result_ack = json.dumps(data_ack)
                s.send(result_ack+"\r\n")
                print ("Message sent to the server: \n"+result_ack)
                server_msg = s.recv(1024)
                print ("Message received from the server: \n"+json.dumps(server_msg))
            elif (json.loads(server_msg)["OrderName"]).encode("utf-8") == "Walk":
                wA.runOnRobot(nao)
                data_ack = {'From':'193.48.125.67', 'To':(json.loads(server_msg)["From"]).encode("utf-8"), 'MsgType':'Ack', 'OrderAccepted':True}
                result_ack = json.dumps(data_ack)
                s.send(result_ack+"\r\n")
                print ("Message sent to the server: \n"+result_ack)
                server_msg = s.recv(1024).decode("utf-8")
                print ("Message received from the server: \n"+server_msg)
    
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
     
