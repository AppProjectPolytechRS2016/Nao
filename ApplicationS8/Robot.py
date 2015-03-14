import sys

from abc import ABCMeta

class Robot(object):
    
       __metaclass__ = ABCMeta

       def __init__(self, name, IPAdress, port, robotState, videoState, type):
       
              self.name = name
              self.IPAdress = IPAdress      # "127.0.0.1"
              self.port = port             # 9559
              self.robotState = robotState
              self.videoState = videoState
              self.type = type
              
Robot.register(tuple)

assert issubclass(tuple, Robot)
assert isinstance((), Robot)
       
        
