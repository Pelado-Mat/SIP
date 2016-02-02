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


class _Singleton(type):
    __instances = {}
    __singleton_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            with cls.__singleton_lock:
                if cls not in cls.__instances:
                    cls.__instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls.__instances[cls]


class Singleton(_Singleton('SingletonMeta', (object,), {})): pass


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


class BaseControlPlugin(Singleton):
    """
    Base Class to implement Control Plugins interfaces
    """

    def __init__(self, defaultParameters):
        """
        Construct a new Control Plugin object.
        :params: options
            dictionary with the default options that the plugin must use
        :return: returns nothing
        """
        self._lock = threading.RLock()
        self._platform = ''
        self._options = [] # List of options
        self._parameters = self.load_params(defaultParameters)
        self._maxOnStations = 5  # Max Numer of stations that can be powered at the same time.- Ignored
        self._stationState = []  # list of one byte per station, 1 = turn on, 0 = turn off


    def load_params(self, defaultParameters):
        paramFile = os.path.join(".", "data", self.__class__.__name__) + ".json"
        try:
            with open(paramFile, 'r') as f:  # Read the settings from file
                params = json.load(f)
        except IOError:  # If file does not exist create file with defaults.
            if len(defaultParameters.keys()) == 0:
                raise NameError('No default nor json file: ' + paramFile)
            params = defaultParameters
            with open(paramFile, 'w') as f:
                json.dump(params, f)
        return params

    @property
    def platform(self):
        return self._platform

    @property
    def maxStations(self):
        raise NameError('Must be implemented in the derived class')

    @property
    def nStations(self):
        return len(self._stationState)

#    @nStations.setter
#     def nStations(self, number):
#          """
#         Must be overloaded by the child class to make the change persistent
#         @param self:
#        @param number: #
#        @ return:
#         """
#        if self.nStations <= number:
#            self._stationState = self._stationState + [0] * ( number - self.nStations)
#         else:
#             self._stationState = self._stationState[:number]

    @property
    def _params(self):
        return self._parameters

    @_params.setter
    def _params(self, params):
        """ Must be overloaded to make sure that the changes are activated in the current live
            The "user" must only change the options parameters
        """
        # TODO: Add some simple validations
        self._parameters = params
        paramFile = os.path.join(".", "data", self.__class__.__name__) + ".json"
        with open(paramFile, 'w') as f:
            json.dump(params, f)

    @property
    def stations(self):
        """
        Return the list of stations available and the current State
        """
        with self._lock:
            return self._stationState

    @stations.setter
    def stations(self, newStationsState):
        raise NameError('Must be implemented in the derived class')

    def changeStationNumber(self, newStationNumber):
        raise NameError('Must be implemented in the derived class')

    @property
    def options(self):
        """
        Return the options, including the default current value
        @param number:
        @return:
        """

        r_opt = []
        for opt in self._options:
            r_opt = r_opt + [opt + [self._params[opt[0]]]]

        return r_opt

    @options.setter
    def options(self, n_opt):
        """
        Set the new options, the program MUST be restarted, does not changes the current configuration
        @param number:
        @return:
        """
        print "N Opts:", str(n_opt)
        p = self._params

        for opt in n_opt:
            p[opt[0]] = opt[5]
        self._params = p


    @property
    def maxOnStations(self):
        """
        Return the maximun number of stations
        that can be on at the same time
        """
        return self._maxOnStations

    def runningStations(self):
        """
        Return a list of the running stations
        """
        return [i for i, x in enumerate(self.stations) if x == 1]

    def rainSense(self):
        """
        Return a boolean, TRUE if rain is detected and the sensor is
        installed
        """
        return False

    def stopStations(self):
        """
        Stop all stations
        if the list is empty, stop all stations
        """
        self.stations = ([0] * len(self._stationState))
        return  self.stations

    def pinCleanUp(self):
        """
        Stop al Stations and clean pin State
        @return:
        """
        raise NameError('Must be implemented in the derived class')


class BaseBoardPlugin(Singleton):
    """
    Base class to implement a HW abstraction layer to control the PINS
    """
    pass

class RaspberryBoard(BaseBoardPlugin):
    """
    Implements RaspBerry PI HW management
    """
    pass

class BeagleboneBoard(BaseBoardPlugin):
    """
    Implements BeagleboneBoard
    """
    pass
