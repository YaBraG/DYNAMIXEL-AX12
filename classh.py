import socketio
import math


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


@sio.on('drive-orders')
def on_message(angle, speed):

    newAngle = round(math.pow((angle + (4/math.pi))*speed*1000, 3), 4)
    if speed > -0.05 and speed < 0.05:
        newAngle = 0

    # newSpeed = round(remap(speed, 0, 1.15, 0, 1023))

    # if angle < 0:
    #     newAngle = round(remap(angle, -3.14, 0, 1024, 2047))

    # if angle > 0:
    #     newAngle = round(remap(angle, 0, 3.14, 0, 1023))

    # if newSpeed < 50:
    #     newAngle = 0

    # motor2Angle = round(remap(newAngle, 0, 2047, -2047, 0))
    # motor2Angle = -motor2Angle
    # if motor2Angle > 1023:
    #     motor2Angle = round(remap(motor2Angle, 1024, 2047, -2047, -1024))
    #     motor2Angle = -motor2Angle
    print(newAngle)


sio.connect('http://192.168.2.11:3000')
sio.wait()
