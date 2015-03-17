'''
Created on 15 mars 2015

@author: NATHAN
'''
from ApplicationS8.Features import Features
from ApplicationS8.Nao import Nao
from ApplicationS8.NaoApplication import NaoApplication

class stopRobot(Features):
    'Common base class for stopRobot feature'
    'The goal of this feature is to stop the robot'


    def __init__(self):
        '''
        Constructor
        '''
        self.name = "stopRobot"
        
    def runFeatureOnRobot(self, Nao):
        # Nao.disconnect()
        