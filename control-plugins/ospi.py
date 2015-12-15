from controlBase import BaseControlPlugin
import gv
import gpio_pins

defaultParameters = {
    'nbrd' = 1,
    'nst_per_board'=8
}

class OspiControl(BaseControlPlugin):
    def __init__(self):
        super(OspiControl,self).__init__(defaultParameters)
        self.nbrd = self.params['nbrd']
        self.nst_per_board =  self.params['nst_per_board']
        self.__stationState = [0] * (self.nbrd + 1) # list of bytes, one byte per board -0 off 1 on)

    def stations(self):
        """
        Return a list of all the stations
        @return:
        """
        return range(self.nbrd*self.nst_per_board)

    def maxStations(self):
        """
        We supose that the board can turn on all stations at the same time

        @return:
            integer
        """
        return (self.nbrd*self.nst_per_board)

    def runningStations(self):
        rs = []
        for board in self.sbits:


