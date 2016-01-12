# !/usr/bin/python
# -*- coding: utf-8 -*-

#####################################################################
# Control Class to replace the relay_board Plugin                   #
# MV: Only tested on Raspberry PI                                   #
#
#####################################################################
from controlBase import BaseControlPlugin
import time

try:
    import RPi.GPIO as GPIO
except ImportError:
    try:
        import Adafruit_BBIO.GPIO as GPIO
    except ImportError:
        GPIO = None
        print 'No GPIO module was loaded from GPIO Pins module'

try:
    import pigpio
    use_pigpio = True
except ImportError:
    use_pigpio = False

class RelayBoardControl(BaseControlPlugin):
    def __init__(self):
        defParams = self.__autoconfigure_parms()
        super(RelayBoardControl, self).__init__(defParams)
        # Parameters
        self.nStations = self.params['nStations']
        self._relay_pins = self.params['relay_pins']
        self._platform = self.params['platform']
        self._pin_map = self.params['pin_map']
        self._pin_rain_sense = self.params['pin_rain_sense']
        self._pin_relay = self.params['pin_relay']
        self._active = self.params['active']
        self._pi = None
        # Internal State
        self._stationState = [0] * (self.nStations)


        if use_pigpio:
            self.__pi = pigpio.pi()
        else:
            if GPIO:
                GPIO.setwarnings(False)
                GPIO.setmode(GPIO.BOARD)  # IO channels are identified by header connector pin numbers. Pin numbers are
        try:
            if GPIO:
                self.__setup_pins()
        except NameError:
            pass

    def __autoconfigure_parms(self):

        defaultParameters = {
            'nStations': 8,
            'maxOnStations': 5,
            'platform': 'pi',
            'pin_map': [],  # Autodected on first run
            'relay_pins': [11,12,13,15,16,18,22,7,3,5,24,26],  # Pins Conected with the relays - relay_board default
            'pin_rain_sense': 8,  # Autodected on first run - relay_board default
            'pin_relay': 10,  # Autodected on first run - relay_board default
            'active': 'high'
        }

        try:
            import pigpio
            use_pigpio = True
        except ImportError:
            use_pigpio = False

        try:
            import RPi.GPIO as GPIO
            defaultParameters['platform'] = 'pi'
            rev = GPIO.RPI_REVISION
            if rev == 1:
                # map 26 physical pins (1based) with 0 for pins that do not have a gpio number
                if use_pigpio:
                    defaultParameters['pin_map'] = [0, 0, 0, 0, 0, 1, 0, 4, 14, 0, 15, 17, 18, 21, 0, 22, 23, 0, 24, 10,
                                                    0, 9,
                                                    25, 11, 8, 0, 7]
                else:
                    defaultParameters['pin_map'] = [0, 0, 0, 0, 0, 5, 0, 7, 8, 0, 10, 11, 12, 13, 0, 15, 16, 0, 18, 19,
                                                    0, 21,
                                                    22, 23, 24, 0, 26]
            elif rev == 2:
                # map 26 physical pins (1based) with 0 for pins that do not have a gpio number
                if use_pigpio:
                    defaultParameters['pin_map'] = [0, 0, 0, 2, 0, 3, 0, 4, 14, 0, 15, 17, 18, 27, 0, 22, 23, 0, 24, 10,
                                                    0, 9,
                                                    25, 11, 8, 0, 7]
                else:
                    defaultParameters['pin_map'] = [0, 0, 0, 0, 0, 5, 0, 7, 8, 0, 10, 11, 12, 13, 0, 15, 16, 0, 18, 19,
                                                    0, 21,
                                                    22, 23, 24, 0, 26]
            elif rev == 3:
                # map 40 physical pins (1based) with 0 for pins that do not have a gpio number
                if use_pigpio:
                    defaultParameters['pin_map'] = [0, 0, 0, 2, 0, 3, 0, 4, 14, 0, 15, 17, 18, 27, 0, 22, 23, 0, 24, 10,
                                                    0, 9,
                                                    25, 11, 8, 0, 7, 0, 0, 5, 0, 6, 12, 13, 0, 19, 16, 26, 20, 0, 21]
                else:
                    defaultParameters['pin_map'] = [0, 0, 0, 3, 0, 5, 0, 7, 8, 0, 10, 11, 12, 13, 0, 15, 16, 0, 18, 19,
                                                    0, 21,
                                                    22, 23, 24, 0, 26, 0, 0, 29, 0, 31, 32, 33, 0, 35, 36, 37, 38, 0,
                                                    40]
            else:
                print 'Unknown pi pin revision.  Using pin mapping for rev 3'
        except ImportError:
            try:
                import \
                    Adafruit_BBIO.GPIO as GPIO  # Required for accessing General Purpose Input Output pins on Beagle Bone Black
                defaultParameters['pin_map'] = [None] * 11  # map only the pins we are using
                defaultParameters['pin_map'].extend(['P9_' + str(i) for i in range(11, 17)])
                defaultParameters['platform'] = 'bo'
            except ImportError:
                defaultParameters['pin_map'] = [i for i in range(
                    27)]  # assume 26 pins all mapped.  Maybe we should not assume anything, but...
                defaultParameters['platform'] = ''  # if no platform, allows program to still run.
                print 'No GPIO module was loaded from GPIO Pins module'

        # Autodetect the rain sensors pin
        try:
            if defaultParameters['platform'] == 'pi':  # If this will run on Raspberry Pi:
                GPIO.setmode(GPIO.BOARD)
                GPIO.setwarnings(False)
                defaultParameters['pin_rain_sense'] = defaultParameters['pin_map'][20]
                defaultParameters['pin_relay'] = defaultParameters['pin_map'][21]
            elif defaultParameters['platform'] == 'bo':  # If this will run on Beagle Bone Black:
                defaultParameters['pin_rain_sense'] = defaultParameters['pin_map'][15]
                defaultParameters['pin_relay'] = defaultParameters['pin_map'][16]
        except AttributeError:
            pass

        return defaultParameters

    def __setup_pins(self):
        """
        Define and setup GPIO pins for shift register operation
        @return:
        """

        try:
            import pigpio
            use_pigpio = True
            self.__pi =  pigpio.pi()
        except ImportError:
            use_pigpio = False
        try:
            for i in range(len(self._relay_pins)):
                time.sleep(0.1)
                if use_pigpio:
                    self__pi.set_mode(self._pin_map[i], pigpio.OUTPUT)
                else:
                    GPIO.setup(self._relay_pins[i], GPIO.OUT)

                if self._active == 'low':
                    if use_pigpio:
                        self__pi.write(self._relay_pins[i], 1)
                    else:
                        GPIO.output(self._relay_pins[i], GPIO.HIGH)
                else:
                    if use_pigpio:
                        self__pi.write(self._relay_pins[i], 0)
                    else:
                        GPIO.output(self._relay_pins[i], GPIO.LOW)
        except:
            print "Problems seting pins!!"
            pass

    @BaseControlPlugin.stations.setter
    def stations(self, newStationState):
        """
        Change the state of the board to the
        @param stationState: # list of one byte per station, 1 = turn on, 0 = turn off
        @return:
            [] - the new station State
        """
        if len(newStationState) != len(self._stationState):
            raise NameError("ERROR: The number of stations is not equal")

        with self.lock:
            for i in range(self.nStations):
                try:
                    if gv.srvals[i]:  # if station is set to on
                        if self._active == 'low':  # if the relay type is active low, set the output low
                            if gv.use_pigpio:
                                pi.write(self._relay_pins[i], 0)
                            else:
                                GPIO.output(self._relay_pins[i], GPIO.LOW)
                        else:  # otherwise set it high
                            if gv.use_pigpio:
                                pi.write(self._relay_pins[i], 1)
                            else:
                                GPIO.output(self._relay_pins[i], GPIO.HIGH)
                                #                    print 'relay switched on', i + 1, "pin", relay_pins[i]  #  for testing #############
                    else:  # station is set to off
                        if self._active == 'low':  # if the relay type is active low, set the output high
                            if gv.use_pigpio:
                                pi.write(self._relay_pins[i], 1)
                            else:
                                GPIO.output(self._relay_pins[i], GPIO.HIGH)
                        else:  # otherwise set it low
                            if gv.use_pigpio:
                                pi.write(self._relay_pins[i], 0)
                            else:
                                GPIO.output(self._relay_pins[i], GPIO.LOW)
                                #                    print 'relay switched off', i + 1, "pin", relay_pins[i]  #  for testing ############
                except Exception, e:
                    print "Problem switching relays", e, self._relay_pins[i]
                    pass
        self._stationState = newStationState
        return self._stationState


import gv

gv.scontrol = RelayBoardControl()
