from __future__ import print_function
import sys
import time
import serial

isPython3 = sys.version_info >= (3,0)

    


class DataLogger(serial.Serial):

    BAUDRATE = 9600
    INIT_TIMEOUT = 1.0 

    def __init__(self,port, logfile, timeout=10.0):
        super(DataLogger,self).__init__(port, self.BAUDRATE,timeout=timeout)
        time.sleep(self.INIT_TIMEOUT)
        self.logfile = logfile
        self.clearInWaiting()

    def clearInWaiting(self):
        while self.inWaiting() > 0:
            self.read()

    def run(self):
        fid = open(self.logfile,'w')
        while 1:
            line = self.readline()
            line = line.strip()
            if isPython3:
                line = str(line,encoding='ascii')
            lineList = line.split(' ')

            error = False
            try:
                secs = int(lineList[0])
                curr = int(lineList[1])
            except:
                error = True

            if error:
                errMsg = 'read error'
                print(errMsg)
                fid.write(errMsg + '\n')
            else:
                print(secs,curr)
                fid.write('{0} {1}\n'.format(secs, curr))
            fid.flush()

        fid.close()


            
# -----------------------------------------------------------------------------
if __name__ == '__main__':

    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        port = '/dev/ttyUSB0'

    if len(sys.argv) > 2:
        logfile = sys.argv[2]
    else:
        logfile = 'log.txt'

    dev = DataLogger(port,logfile)
    dev.run()

