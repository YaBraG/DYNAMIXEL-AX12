from AX12 import Ax12
import math
import socketio


def remap(x, oMin, oMax, nMin, nMax):

    # range check
    if oMin == oMax:
        print("Warning: Zero input range")
        return None

    if nMin == nMax:
        print("Warning: Zero output range")
        return None

    # check reversed input range
    reverseInput = False
    oldMin = min(oMin, oMax)
    oldMax = max(oMin, oMax)
    if not oldMin == oMin:
        reverseInput = True

    # check reversed output range
    reverseOutput = False
    newMin = min(nMin, nMax)
    newMax = max(nMin, nMax)
    if not newMin == nMin:
        reverseOutput = True

    portion = (x-oldMin)*(newMax-newMin)/(oldMax-oldMin)
    if reverseInput:
        portion = (oldMax-x)*(newMax-newMin)/(oldMax-oldMin)

    result = portion + newMin
    if reverseOutput:
        result = newMax - portion

    return result


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

    def start(self):
        self.motor1.enable_torque()
        self.motor2.enable_torque()

    def move(self):
        # speedMult1 = math.cos(self.angle)
        # speedMult2 = math.sin(self.angle)
        # mSpeed1 = self.speed * speedMult1
        # mSpeed2 = self.speed * speedMult2
        # print(mSpeed1, mSpeed2)
        self.motor1.set_moving_speed(self.angle)
        self.motor2.set_moving_speed(- self.angle)

    def setAngle(self, angle):
        self.angle = angle

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

drive = Drive(1, 2)


@sio.event
def connect():
    print('connection established')
    sio.emit("ID", 'python-servo-client')
    drive.start()
    while (1):
        drive.move()


@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})


@sio.event
def disconnect():
    print('disconnected from server')
    drive.stop()


@sio.on('drive-orders')
def on_message(angle, speed):
    # newSpeed = 0
    # newAngle = 0
    if speed < 0:
        newSpeed = round(remap(speed, -1, 0, 1024, 2047))

    if speed > 0:
        newSpeed = round(remap(speed, 0, 1, 0, 1023))

    if angle < 0:
        newAngle = round(remap(angle, -1, 0, 1024, 2047))

    if angle > 0:
        newAngle = round(remap(angle, 0, 1, 0, 1023))

    drive.setAngle(newAngle)
    drive.setSpeed(newSpeed)


sio.connect('http://192.168.2.11:3000')
sio.wait()
