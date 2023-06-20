from AX12 import Ax12
import math
import socketio
import time


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

# create AX12 instance with motors ID
motor1 = Ax12(1)
motor2 = Ax12(2)
motor1.set_max_voltage_limit(160)
motor2.set_max_voltage_limit(160)
motor1.enable_torque()
motor2.enable_torque()
motor1.set_torque_limit(1023)
motor2.set_torque_limit(1023)

try:
    @sio.event
    def connect():
        print('connection established')
        sio.emit("ID", 'python-servo-client')

    @sio.event
    def my_message(data):
        print('message received with ', data)
        sio.emit('my response', {'response': 'my response'})

    @sio.event
    def disconnect():
        print('disconnected from server')
        motor1.disable_torque()
        motor2.disable_torque()

    @sio.on('drive-orders')
    def on_message(angle, speed):
        # newSpeed = 0
        # newAngle = 0

        newSpeed = round(remap(speed, 0, 1.15, 0, 1023))

        if angle < 0:
            newAngle = round(remap(angle, -3.14, 0, 1024, 2047))

        if angle > 0:
            newAngle = round(remap(angle, 0, 3.14, 0, 1023))

        if newSpeed < 50:
            newAngle = 0

        motor2Angle = round(remap(newAngle, 0, 2047, -2047, 0))
        motor2Angle = -motor2Angle
        if motor2Angle > 1023:
            motor2Angle = round(remap(motor2Angle, 1024, 2047, -2047, -1024))
            motor2Angle = -motor2Angle
        motor1.set_moving_speed(1023)
        motor2.set_moving_speed(2040)

    sio.connect('http://192.168.2.11:3000')
    sio.wait()

except KeyboardInterrupt:
    time.sleep(1)
    motor1.set_moving_speed(0)
    motor2.set_moving_speed(0)
    motor1.disable_torque()
    motor2.disable_torque()
