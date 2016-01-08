# !/usr/bin/python
# -*- coding: utf-8 -*-

#####################################################################
# Control Class to support the OSI HW,                              #
# Mainly using the gpio_pins logic                                  #
# MV: I do not have OSPI HW!!! UNTESTED!
#
#####################################################################
from controlBase import BaseControlPlugin
try:
    import RPi.GPIO as GPIO
except ImportError:
    try:
        import Adafruit_BBIO.GPIO as GPIO
    except ImportError:
        GPIO = None
        print 'No GPIO module was loaded from GPIO Pins module'


class OspyBoardControl(BaseControlPlugin):

    def __init__(self):
        defParams = self.__autoconfigure_parms()
        print defParams
        super(BoardControl, self).__init__(defParams)
        # Parameters
        self.nbrd = self.params['nbrd']
        self.maxOnStations = self.params['maxOnStations']

        # Private
        self.__nst_per_board = self.params['nst_per_board']
        self.__platform = self.params['platform']
        self.__pin_map = self.params['pin_map']
        self.__pin_rain_sense = self.params['pin_rain_sense']
        self.__pin_relay = self.params['pin_relay']
        self.__pin_sr = self.params['pin_sr']
        self.__pi = None
        # Internal State
        self.__stationState = [0] * (self.nbrd * self.__nst_per_board)

        try:
            import pigpio
            use_pigpio = True
        except ImportError:
            use_pigpio = False

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
        'nbrd': 1,
        'nst_per_board': 8,
        'maxOnStations': 5,
        'platform': '',  # Autodected on first run "pi" for RaspBerry | "bo" for Beagle Bone Black
        'pin_map': [],  # Autodected on first run
        'pin_rain_sense': 1,  # Autodected on first run
        'pin_relay': 1,  # Autodected on first run
        'pin_sr': {'dat': 1, 'clk': 1, 'noe': 1, 'lat': 1}  # Autodected on first run
        }

        try:
            import pigpio
            use_pigpio = True
        except ImportError:
            use_pigpio = False

        # Will try to autodetect the pin out and the type of board the first time the module is loaded
        try:
            import RPi.GPIO as GPIO
            defaultParameters['platform'] = 'pi'
            rev = GPIO.RPI_REVISION
            if rev == 1:
                # map 26 physical pins (1based) with 0 for pins that do not have a gpio number
                if use_pigpio:
                    defaultParameters['pin_map'] = [0, 0, 0, 0, 0, 1, 0, 4, 14, 0, 15, 17, 18, 21, 0, 22, 23, 0, 24, 10, 0, 9,
                                                    25, 11, 8, 0, 7]
                else:
                    defaultParameters['pin_map'] = [0, 0, 0, 0, 0, 5, 0, 7, 8, 0, 10, 11, 12, 13, 0, 15, 16, 0, 18, 19, 0, 21,
                                                    22, 23, 24, 0, 26]
            elif rev == 2:
                # map 26 physical pins (1based) with 0 for pins that do not have a gpio number
                if use_pigpio:
                    defaultParameters['pin_map'] = [0, 0, 0, 2, 0, 3, 0, 4, 14, 0, 15, 17, 18, 27, 0, 22, 23, 0, 24, 10, 0, 9,
                                                    25, 11, 8, 0, 7]
                else:
                    defaultParameters['pin_map'] = [0, 0, 0, 0, 0, 5, 0, 7, 8, 0, 10, 11, 12, 13, 0, 15, 16, 0, 18, 19, 0, 21,
                                                    22, 23, 24, 0, 26]
            elif rev == 3:
                # map 40 physical pins (1based) with 0 for pins that do not have a gpio number
                if use_pigpio:
                    defaultParameters['pin_map'] = [0, 0, 0, 2, 0, 3, 0, 4, 14, 0, 15, 17, 18, 27, 0, 22, 23, 0, 24, 10, 0, 9,
                                                    25, 11, 8, 0, 7, 0, 0, 5, 0, 6, 12, 13, 0, 19, 16, 26, 20, 0, 21]
                else:
                    defaultParameters['pin_map'] = [0, 0, 0, 3, 0, 5, 0, 7, 8, 0, 10, 11, 12, 13, 0, 15, 16, 0, 18, 19, 0, 21,
                                                    22, 23, 24, 0, 26, 0, 0, 29, 0, 31, 32, 33, 0, 35, 36, 37, 38, 0, 40]
            else:
                print 'Unknown pi pin revision.  Using pin mapping for rev 3'
        except ImportError:
            try:
                import Adafruit_BBIO.GPIO as GPIO  # Required for accessing General Purpose Input Output pins on Beagle Bone Black
                defaultParameters['pin_map'] = [None] * 11  # map only the pins we are using
                defaultParameters['pin_map'].extend(['P9_' + str(i) for i in range(11, 17)])
                defaultParameters['platform'] = 'bo'
            except ImportError:
                defaultParameters['pin_map'] = [i for i in range(27)]  # assume 26 pins all mapped.  Maybe we should not assume anything, but...
                defaultParameters['platform'] = ''  # if no platform, allows program to still run.
                print 'No GPIO module was loaded from GPIO Pins module'

        # Autodetect the rain sensors pin
        try:
            if defaultParameters['platform'] == 'pi':  # If this will run on Raspberry Pi:
                GPIO.setmode(GPIO.BOARD)
                GPIO.setwarnings(False)
                defaultParameters['pin_rain_sense'] = defaultParameters['pin_map'][8]
                defaultParameters['pin_relay'] = defaultParameters['pin_map'][10]
            elif defaultParameters['platform'] == 'bo':  # If this will run on Beagle Bone Black:
                defaultParameters['pin_rain_sense'] = defaultParameters['pin_map'][15]
                defaultParameters['pin_relay'] = defaultParameters['pin_map'][16]
        except AttributeError:
            pass

        # Autodefine the GPIO pins for shift register operation
        try:
            if defaultParameters['platform'] == 'pi':  # If this will run on Raspberry Pi:
                if not use_pigpio:
                    GPIO.setmode(GPIO.BOARD)  # IO channels are identified by header connector pin numbers. Pin numbers are always the same regardless of Raspberry Pi board revision.
                defaultParameters['pin_sr']['dat'] = defaultParameters['pin_map'][13]
                defaultParameters['pin_sr']['clk'] = defaultParameters['pin_map'][7]
                defaultParameters['pin_sr']['noe'] = defaultParameters['pin_map'][11]
                defaultParameters['pin_sr']['lat'] = defaultParameters['pin_map'][15]
            elif defaultParameters['platform'] == 'bo':  # If this will run on Beagle Bone Black:
                defaultParameters['pin_sr']['dat'] = defaultParameters['pin_map'][11]
                defaultParameters['pin_sr']['clk'] = defaultParameters['pin_map'][13]
                defaultParameters['pin_sr']['noe'] = defaultParameters['pin_map'][14]
                defaultParameters['pin_sr']['lat'] = defaultParameters['pin_map'][12]
        except AttributeError:
            pass

        return defaultParameters

    def __setup_pins(self):
        """
        Define and setup GPIO pins for shift register operation
        @return:
        """
        if self.__pi:
            # GPIO
            self.__pi.set_mode(self.__pin_sr['noe'], pigpio.OUTPUT)
            self.__pi.set_mode(self.__pin_sr['clk'], pigpio.OUTPUT)
            self.__pi.set_mode(self.__pin_sr['dat'], pigpio.OUTPUT)
            self.__pi.set_mode(self.__pin_sr['lat'], pigpio.OUTPUT)
            self.__pi.write(self.__pin_sr['noe'], 1)
            self.__pi.write(self.__pin_sr['clk'], 0)
            self.__pi.write(self.__pin_sr['dat'], 0)
            self.__pi.write(self.__pin_sr['lat'], 0)
            # Rain Sensor
            self.__pi.set_mode(self.__pin_rain_sense, pigpio.INPUT)
            self.__pi.set_mode(self.__pin_relay, pigpio.OUTPUT)
        else:
            # GPIO
            GPIO.setup(self.__pin_sr['noe'], GPIO.OUT)
            GPIO.setup(self.__pin_sr['clk'], GPIO.OUT)
            GPIO.setup(self.__pin_sr['dat'], GPIO.OUT)
            GPIO.setup(self.__pin_sr['lat'], GPIO.OUT)
            GPIO.output(self.__pin_sr['noe'], GPIO.HIGH)
            GPIO.output(self.__pin_sr['clk'], GPIO.LOW)
            GPIO.output(self.__pin_sr['dat'], GPIO.LOW)
            GPIO.output(self.__pin_sr['lat'], GPIO.LOW)
            # Rain Sensor
            GPIO.setup(self.__pin_rain_sense, GPIO.IN)
            GPIO.setup(self.__pin_relay, GPIO.OUT)

    def __disableShiftRegisterOutput(self):
        """Disable output from shift register."""
        try:
            if self.__pi:
                pi.write(self.__pin_sr['noe'], 1)
            else:
                GPIO.output(self.__pin_sr['noe'], GPIO.HIGH)
        except Exception:
            pass

    def __enableShiftRegisterOutput(self):
        """Enable output from shift register."""
        try:
            if self.__pi:
                self.__pi.write(self.__pin_sr['noe'], 0)
            else:
                GPIO.output(self.__pin_sr['noe'], GPIO.LOW)
        except Exception:
            pass

    def __setShiftRegister(self, newStationState):
        """Set the state of each output pin on the shift register from the srvals list."""
        nst = len(self.__stationState)
        srvals = newStationState
        try:
            if self.__pi:
                self.__pi.write(self.__pin_sr['clk'], 0)
                self.__pi.write(self.__pin_sr['lat'], 0)
                for s in range(nst):
                    self.__pi.write(self.__pin_sr['clk'], 0)
                    if srvals[nst - 1 - s]:
                        self.__pi.write(self.__pin_sr['dat'], 1)
                    else:
                        self.__pi.write(self.__pin_sr['dat'], 0)
                    self.__pi.write(self.__pin_sr['clk'], 1)
                self.__pi.write(self.__pin_sr['lat'], 1)
            else:
                GPIO.output(self.__pin_sr['clk'], GPIO.LOW)
                GPIO.output(self.__pin_sr['lat'], GPIO.LOW)
                for s in range(nst):
                    GPIO.output(self.__pin_sr['clk'], GPIO.LOW)
                    if srvals[nst - 1 - s]:
                        GPIO.output(self.__pin_sr['dat'], GPIO.HIGH)
                    else:
                        GPIO.output(self.__pin_sr['dat'], GPIO.LOW)
                    GPIO.output(self.__pin_sr['clk'], GPIO.HIGH)
                GPIO.output(self.__pin_sr['lat'], GPIO.HIGH)
        except Exception:
            pass

    @BaseControlPlugin.stations.setter
    def stations(self, newStationState):
        """
        Change the state of the board to the
        @param stationState: # list of one byte per station, 1 = turn on, 0 = turn off
        @return:
            [] - the new station State
        """
        if len(newStationState) != len(self.__stationState):
            raise NameError("ERROR: The number of stations is not equal")

        with self.lock:
            if GPIO:
                self.__disableShiftRegisterOutput()
                self.__setShiftRegister(newStationState)
                self.__enableShiftRegisterOutput()
                self.__stationState = newStationState
            else:
                print "GPIO not defined, cannot change the stations!"
        return self.__stationState



import gv
gv.scontrol = OspyBoardControl()