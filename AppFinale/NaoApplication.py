import socket
import json
import sys
import math

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
    'NAOIP_GRIS: 193.48.125.62'  
    nao = Nao("193.48.125.63",9559)
    
    'Initialization of the different features'  
    iR = initRobot()
    sR = stopRobot()
    wA = Walk()
    mR = Move(1,0,0)
    tP = TakePicture()
    mM = Mime(0,0,0,0,0,0)
    kR = Kick()
    
    'Adding the features to the list of features of the NaoAppliaction instance'
    na.features.append(iR)
    na.features.append(sR)
    na.features.append(wA)
    na.features.append(mR)
    na.features.append(tP)
    na.features.append(mM)
    na.features.append(kR)
    
    "Getting a list of Features name"
    NaoFeaturesList = []
    for i in range (0, len(na.features)):
        featureName = na.features[i].name
        NaoFeaturesList.append(featureName)
    print ("Nao Features List:")
    print NaoFeaturesList
    
    
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
        s.connect(('193.48.125.64', 6030))
    except socket.error:
        print 'Socket connection failed! Host is unreachable! Exiting program!'
        s.close()
        sys.exit(0)
    
    'Sending the Ident Message to the Server'
    try:
        s.send(result_ident+"\r\n")
    except socket.error, e:
        print "Error sending data: %s" % e
        sys.exit(1)
    
    'Printing the Message sent'
    print ("Message sent to the server: \n"+result_ident)
    
    'Receiving Message from the Server'
    #server_msg = {u'From':'193.48.125.67', u'To':'193.48.125.68', u'MsgType':'Order', u'OrderName':'ConnectTo'}
    try:
        server_msg = s.recv(1024).decode("utf-8")
    except socket.error, e:
        print "Error receiving data: %s" % e
        sys.exit(1)
    print ("Message received from the server: \n"+server_msg)
    
    'Main LOOP of the application'
    'We are testing here the JSON received to run the right feature'
    while (json.loads(server_msg)["MsgType"]).encode("utf-8") != "End":
        if (json.loads(server_msg)["MsgType"]).encode("utf-8") == "Order":
            if (json.loads(server_msg)["OrderName"]).encode("utf-8") == "ConnectTo":
                save = (json.loads(server_msg)["From"]).encode("utf-8");
                data_ack = {'From':'193.48.125.67', 'To':(json.loads(server_msg)["From"]).encode("utf-8"), 'MsgType':'Ack', 'OrderAccepted':True, 'FeatureList':NaoFeaturesList}
                result_ack = json.dumps(data_ack)
                try:
                    s.send(result_ack+"\r\n")
                except socket.error, e:
                    print "Error sending data: %s" % e
                    s.close()
                    sys.exit(1)
                print ("Message sent to the server: \n"+result_ack)
                iR.runOnRobot(nao)
                try:
                    server_msg = s.recv(1024).decode("utf-8")
                except socket.error, e:
                    print "Error receiving data: %s" % e
                    sys.exit(1)
                print ("Message received from the server: \n"+server_msg)
                
                while (json.loads(server_msg)["From"]).encode("utf-8") != save:
                    data_ack = {'From':'193.48.125.67', 'To':(json.loads(server_msg)["From"]).encode("utf-8"), 'MsgType':'Ack', 'OrderAccepted':False}
                    unavailable_ack = json.dumps(data_ack)
                    try:
                        s.send(unavailable_ack+"\r\n")
                    except socket.error, e:
                        print "Error sending data: %s" % e
                        s.close()
                        sys.exit(1)
                    print ("Message sent to the server: \n"+unavailable_ack)
                    
                    try:
                        server_msg = s.recv(1024).decode("utf-8")
                    except socket.error, e:
                        print "Error receiving data: %s" % e
                        sys.exit(1)
                    print ("Message received from the server: \n"+server_msg)
                    
                if (json.loads(server_msg)["From"]).encode("utf-8") == save:
                
                    if (json.loads(server_msg)["OrderName"]).encode("utf-8") == "Init":
                        data_ack = {'From':'193.48.125.67', 'To':(json.loads(server_msg)["From"]).encode("utf-8"), 'MsgType':'Ack', 'OrderAccepted':True}
                        result_ack = json.dumps(data_ack)
                        try:
                            s.send(result_ack+"\r\n")
                        except socket.error, e:
                            print "Error sending data: %s" % e
                            s.close()
                            sys.exit(1)
                        print ("Message sent to the server: \n"+result_ack)
                        iR.runOnRobot(nao)
                        try:
                            server_msg = s.recv(1024).decode("utf-8")
                        except socket.error, e:
                            print "Error receiving data: %s" % e
                            s.close()
                            sys.exit(1)
                        print ("Message received from the server: \n"+server_msg)
                        
                    elif (json.loads(server_msg)["OrderName"]).encode("utf-8") == "Stop":
                        data_ack = {'From':'193.48.125.67', 'To':(json.loads(server_msg)["From"]).encode("utf-8"), 'MsgType':'Ack', 'OrderAccepted':True, 'End':True}
                        result_ack = json.dumps(data_ack)
                        try:
                            s.send(result_ack+"\r\n")
                        except socket.error, e:
                            print "Error sending data: %s" % e
                            s.close()
                            sys.exit(1)
                        print ("Message sent to the server: \n"+result_ack)
                        data_log = {'From':'193.48.125.67', 'To':'193.48.125.64', 'MsgType':'Logout'}
                        result_logout = json.dumps(data_log)
                        try:
                            s.send(result_logout+"\r\n")
                        except socket.error, e:
                            print "Error sending data: %s" % e
                            s.close()
                            sys.exit(1)
                        print ("Message sent to the server: \n"+result_logout)
                        sR.runOnRobot(nao)
                        #try:
                        #    server_msg = s.recv(1024).decode("utf-8")
                        #except socket.error, e:
                        #   print "Error receiving data: %s" % e
                        #    s.close()
                        #    sys.exit(1)
                        #s.close()
                        sys.exit(1)
                        print ("Message received from the server: \n"+server_msg)
                        
                    elif (json.loads(server_msg)["OrderName"]).encode("utf-8") == "Move":
                        data_ack = {'From':'193.48.125.67', 'To':(json.loads(server_msg)["From"]).encode("utf-8"), 'MsgType':'Ack', 'OrderAccepted':True}
                        result_ack = json.dumps(data_ack)
                        try:
                            s.send(result_ack+"\r\n")
                        except socket.error, e:
                            print "Error sending data: %s" % e
                            s.close()
                            sys.exit(1)
                        print ("Message sent to the server: \n"+result_ack)
                        
                        'Test if the order came from the Tab or the Kinect'
                        
                        if  "XValue" not in json.dumps(server_msg).encode("utf-8"):
                            mR.runOnRobot(nao)
                        else:
                            moveRobot = Move(json.loads(server_msg)["XValue"]*0.01,json.loads(server_msg)["YValue"]*0.01,math.pi*json.loads(server_msg)["ThetaValue"]/180)
                            moveRobot.runOnRobot(nao)
                           
                        try:
                            server_msg = s.recv(1024).decode("utf-8")
                        except socket.error, e:
                            print "Error receiving data: %s" % e
                            s.close()
                            sys.exit(1)
                        print ("Message received from the server: \n"+json.dumps(server_msg))
                    
                        
                    elif (json.loads(server_msg)["OrderName"]).encode("utf-8") == "TakePicture":
                        data_ack = {'From':'193.48.125.67', 'To':(json.loads(server_msg)["From"]).encode("utf-8"), 'MsgType':'Ack', 'OrderAccepted':True}
                        result_ack = json.dumps(data_ack)
                        try:
                            s.send(result_ack+"\r\n")
                        except socket.error, e:
                            print "Error sending data: %s" % e
                            s.close()
                            sys.exit(1)
                        print ("Message sent to the server: \n"+result_ack)
                        tP.runOnRobot(nao)
                        try:
                            server_msg = s.recv(1024).decode("utf-8")
                        except socket.error, e:
                            print "Error receiving data: %s" % e
                            s.close()
                            sys.exit(1)
                        print ("Message received from the server: \n"+json.dumps(server_msg))
                    
                    elif (json.loads(server_msg)["OrderName"]).encode("utf-8") == "Kick":
                        data_ack = {'From':'193.48.125.67', 'To':(json.loads(server_msg)["From"]).encode("utf-8"), 'MsgType':'Ack', 'OrderAccepted':True}
                        result_ack = json.dumps(data_ack)
                        try:
                            s.send(result_ack+"\r\n")
                        except socket.error, e:
                            print "Error sending data: %s" % e
                            s.close()
                            sys.exit(1)
                        print ("Message sent to the server: \n"+result_ack)
                        kR.runOnRobot(nao)
                        try:
                            server_msg = s.recv(1024).decode("utf-8")
                        except socket.error, e:
                            print "Error receiving data: %s" % e
                            s.close()
                            sys.exit(1)
                        print ("Message received from the server: \n"+json.dumps(server_msg))
                        
                    elif (json.loads(server_msg)["OrderName"]).encode("utf-8") == "Walk":
                        data_ack = {'From':'193.48.125.67', 'To':(json.loads(server_msg)["From"]).encode("utf-8"), 'MsgType':'Ack', 'OrderAccepted':True}
                        result_ack = json.dumps(data_ack)
                        try:
                            s.send(result_ack+"\r\n")
                        except socket.error, e:
                            print "Error sending data: %s" % e
                            s.close()
                            sys.exit(1)
                        print ("Message sent to the server: \n"+result_ack)
                        wA.runOnRobot(nao)
                        try:
                            server_msg = s.recv(1024).decode("utf-8")
                        except socket.error, e:
                            print "Error receiving data: %s" % e
                            s.close()
                            sys.exit(1)
                        print ("Message received from the server: \n"+server_msg)
                    
                    
                    
                    elif (json.loads(server_msg)["OrderName"]).encode("utf-8") == "Mime":
                        saveMime = (json.loads(server_msg)["From"]).encode("utf-8");
                        data_ack = {'From':'193.48.125.67', 'To':(json.loads(server_msg)["From"]).encode("utf-8"), 'MsgType':'Ack', 'OrderAccepted':True, 'MimeAccepted':True}
                        result_ack = json.dumps(data_ack)
                        try:
                            s.send(result_ack+"\r\n")
                        except socket.error, e:
                            print "Error sending data: %s" % e
                            s.close()
                            sys.exit(1)
                        print ("Message sent to the server: \n"+result_ack)
                        try:
                            server_msg = s.recv(1024).decode("utf-8")
                        except socket.error, e:
                            print "Error receiving data: %s" % e
                            s.close()
                            sys.exit(1)
                        print ("Message received from the server: \n"+server_msg)
                        
                        while (json.loads(server_msg)["From"]).encode("utf-8") != saveMime:
                            data_ack = {'From':'193.48.125.67', 'To':(json.loads(server_msg)["From"]).encode("utf-8"), 'MsgType':'Ack', 'OrderAccepted':False}
                            unavailable_ack = json.dumps(data_ack)
                            try:
                                s.send(unavailable_ack+"\r\n")
                            except socket.error, e:
                                print "Error sending data: %s" % e
                                s.close()
                                sys.exit(1)
                            print ("Message sent to the server: \n"+unavailable_ack)
                            
                            try:
                                server_msg = s.recv(1024).decode("utf-8")
                            except socket.error, e:
                                print "Error receiving data: %s" % e
                                sys.exit(1)
                            print ("Message received from the server: \n"+server_msg)
                            
                        if (json.loads(server_msg)["From"]).encode("utf-8") == saveMime:
                            
                            data_ack = {'From':'193.48.125.67', 'To':(json.loads(server_msg)["From"]).encode("utf-8"), 'MsgType':'Ack', 'OrderAccepted':True}
                            result_ack = json.dumps(data_ack)
                            try:
                                s.send(result_ack+"\r\n")
                            except socket.error, e:
                                print "Error sending data: %s" % e
                                s.close()
                                sys.exit(1)
                            print ("Message sent to the server: \n"+result_ack)
                            
                            'Roll Pitch Yaw'
                            #mimeRobot = Mime(json.loads(server_msg)["JointOrientation"][7],json.loads(server_msg)["JointOrientation"][6],json.loads(server_msg)["JointOrientation"][11],json.loads(server_msg)["JointOrientation"][9],json.loads(server_msg)["JointOrientation"][1],json.loads(server_msg)["JointOrientation"][0],json.loads(server_msg)["JointOrientation"][5],json.loads(server_msg)["JointOrientation"][3])
                            mimeRobot = Mime(json.loads(server_msg)["JointOrientation"][0],json.loads(server_msg)["JointOrientation"][1],json.loads(server_msg)["JointOrientation"][2],json.loads(server_msg)["JointOrientation"][3],json.loads(server_msg)["JointOrientation"][4],json.loads(server_msg)["JointOrientation"][5])
                            mimeRobot.runOnRobot(nao)
                            
                            try:
                                server_msg = s.recv(1024).decode("utf-8")
                            except socket.error, e:
                                print "Error receiving data: %s" % e
                                s.close()
                                sys.exit(1)
                            print ("Message received from the server: \n"+server_msg)
                    
                    
                        
                    elif (json.loads(server_msg)["OrderName"]).encode("utf-8") == "Disconnect":
                        data_ack = {'From':'193.48.125.67', 'To':(json.loads(server_msg)["From"]).encode("utf-8"), 'MsgType':'Ack', 'OrderAccepted':True, 'Disconnected':True}
                        result_ack = json.dumps(data_ack)
                        try:
                            s.send(result_ack+"\r\n")
                        except socket.error, e:
                            print "Error sending data: %s" % e
                            s.close()
                            sys.exit(1)
                        print ("Message sent to the server: \n"+result_ack)
                        try:
                            server_msg = s.recv(1024).decode("utf-8")
                        except socket.error, e:
                            print "Error receiving data: %s" % e
                            s.close()
                            sys.exit(1)
                        print ("Message received from the server: \n"+server_msg)
                        
            elif (json.loads(server_msg)["OrderName"]).encode("utf-8") != "ConnectTo":
                print "The Message received is not a ConnectTo /n"
                data_ack = {'From':'193.48.125.67', 'To':(json.loads(server_msg)["From"]).encode("utf-8"), 'MsgType':'Ack', 'OrderAccepted':False}
                result_ack = json.dumps(data_ack)
                try:
                    s.send(result_ack+"\r\n")
                except socket.error, e:
                    print "Error sending data: %s" % e
                    s.close()
                    sys.exit(1)
                print ("Message sent to the server: \n"+result_ack)
                try:
                    server_msg = s.recv(1024).decode("utf-8")
                except socket.error, e:
                    print "Error receiving data: %s" % e
                    sys.exit(1)
                print ("Message received from the server: \n"+server_msg)
    
    'Closing the socket'
    s.close()
    print ("The socket has been closed")
   
    
if __name__ == "__main__":
    main()
    
     
