from AX12 import Ax12
import socketio

sio = socketio.Client()

# e.g 'COM11' windows or '/dev/ttyUSB0' for Linux/Raspberry
Ax12.DEVICENAME = '/dev/ttyUSB0'
Ax12.BAUDRATE = 1000000

# sets baudrate and opens com port
Ax12.connect()

# create AX12 instance with motors ID
motor1 = Ax12(1)
motor2 = Ax12(2)

motor1.enable_torque()
motor1.set_moving_speed(1023)
motor2.set_moving_speed(500)
motor1.set_torque_limit(1023)

angle1 = 0
angle2 = 0

while True:
    input_pos = int(input("goal pos: "))
    motor1.set_goal_position(input_pos)
