from AX12 import Ax12
import socketio

# 'COM11' windows or '/dev/ttyUSB0' for Linux/Raspberry
Ax12.DEVICENAME = '/dev/ttyUSB0'
Ax12.BAUDRATE = 1000000

# sets baudrate and opens com port
Ax12.connect()

# create AX12 instance with motors ID
motor1 = Ax12(1)
motor2 = Ax12(2)

motor1.set_moving_speed(1023)
motor2.set_moving_speed(1023)

angle1 = 0
angle2 = 0

# Connect to server to recieve/emmit data
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


@sio.on('h-order')
def on_message(h):
    print(h)
    header = (int(h))
    if (header > 1023):
        header = 1023
    motor1.set_goal_position(header)


@sio.on('mouse-order')
def on_message(pitch, yaw):
    print(pitch, yaw)
    angle1 = (int(pitch))
    angle2 = (int(yaw))
    motor1.set_goal_position(angle1)
    motor2.set_goal_position(angle2)


"""
# Enable if manual input wanted
# def user_input():
    # Check to see if user wants to continue
#     ans = input('Continue? : y/n ')
#     if ans == 'n':
#         return False
#     else:
#         return True

# Starts motor (MANUAL INPUT ONLY)
# def main(motor_object):
#     sets goal position based on user input
#     bool_test = True
#     while bool_test:
#         print("\nPosition of dxl ID: %d is %d " %
#               (motor_object.id, motor_object.get_present_position()))
#         # desired angle input
#         input_pos = angle
#         motor_object.set_goal_position(input_pos)
#         print("Position of dxl ID: %d is now: %d " %
#               (motor_object.id, motor_object.get_present_position()))

# return motor_object.id
#   bool_test = user_input()

# pass in AX12 object
# main(my_dxl)

# disconnect
# my_dxl.set_torque_enable(0)
# Ax12.disconnect()
"""

sio.connect('http://192.168.2.11:3000')
sio.wait()
