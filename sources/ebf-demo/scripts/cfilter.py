import time
import math

class ComplementaryFilter(object):
    def __init__(self, gyroWeight=0.95):
        self.gyroWeight = gyroWeight
        self._reset()

    def _reset(self):
        self.last = 0

        self.accelPos = [0, 0, 0]
        self.gyroPos = [0, 0, 0]
        self.filterPos = [0, 0, 0]

    def input(self, vals):
        now = int(round(time.time() * 1000)) 

        # unpack sensor readings
        accelData = vals[0:3]
        gyroData = vals[4:7]

        # convert accelerometer reading to degrees
        self.accelPos = self.calculateAccelPos(*accelData)

        # if this is our first chunk of data, simply accept
        # the accelerometer reads and move on.
        if self.last == 0:
            self.filterPos = self.gyroPos = self.accelPos
            self.last = now
            return

        # calculate the elapsed time (in seconds) since last data.
        # we need this because the gyroscope measures movement in
        # degrees/second.
        dt = (now - self.last)/1000
        self.last = now

        # calculate change in position from gyroscope readings
        gyroDelta = [i * dt for i in gyroData]
        self.gyroPos = [i + j for i, j in zip(self.gyroPos, gyroDelta)]

        # pitch
        self.filterPos[0] = (self.gyroWeight * (self.filterPos[0] + gyroDelta[0])) + (1-self.gyroWeight) * self.accelPos[0]

        # roll
        self.filterPos[1] = (self.gyroWeight * (self.filterPos[1] + gyroDelta[1])) + (1-self.gyroWeight) * self.accelPos[1]


    def calculateAccelPos(self, x, y, z):
        x2 = (x*x);
        y2 = (y*y);
        z2 = (z*z);

        adx = math.atan2(y, math.sqrt(x2 + z2))
        ady = math.atan2(-x, math.sqrt(y2 + z2))

        return [math.degrees(x) for x in [adx, ady, 0]]
