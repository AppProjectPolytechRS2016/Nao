import sys

from abc import ABCMeta

class Features(object):
    
       __metaclass__ = ABCMeta

       def __init__(self, name):
       
              self.name = name
              
Features.register(tuple)

assert issubclass(tuple, Features)
assert isinstance((), Features)
       
        
