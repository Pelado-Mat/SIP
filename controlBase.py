# !/usr/bin/python
# -*- coding: utf-8 -*-

#####################################################################
# Base Class to define the main interface of a Control Plugin       #
# All control Plugins must be inherited from this class #
#####################################################################
import json
import os
import threading

# Thanks Stack Overflow (http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python)
# https://gist.github.com/werediver/4396488

class Singleton(type):
    __instances = {}
    __singleton_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            with cls.__singleton_lock:
                if cls not in cls.__instances:
                    cls.__instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.__instances[cls]

class SingletonMixin(object):
    __singleton_lock = threading.Lock()
    __singleton_instance = None

    @classmethod
    def instance(cls):
        if not cls.__singleton_instance:
            with cls.__singleton_lock:
                if not cls.__singleton_instance:
                    cls.__singleton_instance = cls()
        return cls.__singleton_instance


class BaseControlPlugin:
    """
    Base Class to implement Control Plugins interfaces
    """
    __metaclass__ = Singleton
    def __init__(self, defaultParameters={}):
        """
        Construct a new Control Plugin object.
        :params: options
            dictionary with the default options that the plugin must use
        :return: returns nothing
        """
        self.params = self.load_params(defaultParameters)
        self.__stationState = [] # list of one byte per station, 1 = turn on, 0 = turn off
        
    def load_params(self,defaultParameters):
        paramFile = os.path.join(".", "data", self.__class__.__name__)
        try:
            with open(paramFile, 'r') as f:  # Read the settings from file
                params = json.load(f)
        except IOError: #  If file does not exist create file with defaults.
            if len(defaultParameters.keys()) == 0:
                raise NameError('No default nor json file')
            params = defaultParameters
            with open(paramFile, 'w') as f:
                json.dump(params,f)
        return params

    def stations(self):
        """
        Return the list of stations available and the current State
        """
        return self.__stationState

    def stationsOn(self):
        """
        Return a list of stations that are on at this moment
        """
        return []

    def maxStations(self):
        """
        Return the maximun number of stations
        that can be on at the same time
        """
        return len(self.__stationState)

    def runningStations(self):
        """
        Return a list of the running stations
        """
        return []

    def rainSense(self):
        """
        Return a boolean, TRUE if rain is detected and the sensor is
        installed
        """
        return False


    def stopStations(self, stations=[]):
        """
        Stop the stations listed
        if the list is empty, stop all stations
        """
        return

    def startStations(self, stations=[]):
        """
        Start all the station listed if posible
        The plugin can limit the maximun stations that can be started
        """
        if len(stations) > self.maxStations():
            raise NameError("Tried to start too many stations")
        return

    def stationIsOn(self,station):
        """
        Returns if the station is on
        """
        return false


