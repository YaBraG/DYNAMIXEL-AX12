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

n = 0
@sio.on('drive-orders')
def on_message(angle, speed):
   
    while (n < 10):
        asMultiplier = angle * speed
        # # newAngle = round(math.pow(asMultiplier, 3), 4)
        # newAngle = round(remap(asMultiplier, 0, 180, 0, 1023))
        if speed < 0.05:
            motor1Speed = 0
            motor2Speed = 0
        if angle == 90:
            motor1Speed = 1023
            motor2Speed = 2047
        elif angle == -90:
            motor1Speed = 2047
            motor2Speed = 1023
        elif angle >= 0 and angle < 90:
            motor1Speed = 1023 * speed
            motor2Speed = round(remap(asMultiplier, 0, 90, 0, 2047))
        elif angle > 90 and angle <= 180:
            motor1Speed = round(remap(asMultiplier, 90, 180, 0, 1023))
            motor2Speed = 2047 * speed
        elif angle < 0 and angle > -90:
            motor1Speed = round(remap(asMultiplier, -90, 0, 2047, 0))
            motor2Speed = 1023 * speed
        elif angle < -90 and angle >= -180:
            motor1Speed = 2047 * speed
            motor2Speed = round(remap(asMultiplier, -180, -90, 0, 1023))
        n += 1
        print(motor1Speed + " | " + motor2Speed)


sio.connect('http://192.168.2.11:3000')
sio.wait()
