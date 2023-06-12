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

    newSpeed = round(remap(speed, 0, 1.15, 0, 1023))

    if angle < 0:
        newAngle = round(remap(angle, -3.14, 0, 1024, 2047))

    if angle > 0:
        newAngle = round(remap(angle, 0, 3.14, 0, 1023))

    print(newAngle, newSpeed)


sio.connect('http://192.168.2.17:3000')
sio.wait()
