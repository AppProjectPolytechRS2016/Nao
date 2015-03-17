from abc import ABCMeta
from ApplicationS8.Robot import Robot

class Features:
    __metaclass__ = ABCMeta

    def __init__(self, name):
        self.name = name
    
    def runFeatureOnRobot(self, Robot):
        pass
              
Features.register(tuple)

assert issubclass(tuple, Features)
assert isinstance((), Features)
       
        
