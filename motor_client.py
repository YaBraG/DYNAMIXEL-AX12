from AX12 import Ax12
import math
import socketio

sio = socketio.Client()

# 'COM11' windows or '/dev/ttyUSB0' for Linux/Raspberry
Ax12.DEVICENAME = '/dev/ttyUSB0'
Ax12.BAUDRATE = 1000000

# sets baudrate and opens com port
Ax12.connect()


class Drive:
    def __init__(self, id1, id2):
        self.speed = 0
        self.angle = 0
        self.mId1 = id1
        self.mId2 = id2
        self.motor1 = Ax12(id1)
        self.motor2 = Ax12(id2)

    def stop(self):
        self.motor1.disable_torque()
        self.motor2.disable_torque()

    def go(self):
        speedMult1 = math.cos(self.angle)
        speedMult2 = math.sin(self.angle)
        mSpeed1 = self.speed * speedMult1
        mSpeed2 = self.speed * speedMult2
        self.motor1.enable_torque()
        self.motor2.enable_torque()
        self.motor1.set_moving_speed(mSpeed1)
        self.motor2.set_moving_speed(mSpeed2)

    def setAnlge(self, angle):
        self.angle = angle
        self.go()

    def setSpeed(self, speed):
        self.speed = speed


# create AX12 instance with motors ID
# motor1 = Ax12(1)
# motor2 = Ax12(2)

# motor1.enable_torque()
# motor2.set_moving_speed(500)
# motor1.set_torque_limit(1023)

# angle1 = 0
# angle2 = 0

# while True:
#     input_pos = int(input("goal pos: "))
#     motor1.set_moving_speed(input_pos)
