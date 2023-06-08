from AX12 import Ax12
import socketio
sio = socketio.Client()


# e.g 'COM3' windows or '/dev/ttyUSB0' for Linux
Ax12.DEVICENAME = '/dev/ttyUSB0'

Ax12.BAUDRATE = 1000000

# sets baudrate and opens com port
Ax12.connect()

# create AX12 instance with motors ID
motor1 = 1
motor2 = 2
my_dxl1 = Ax12(motor1)
my_dxl2 = Ax12(motor2)

my_dxl1.set_torque_enable(True)
my_dxl2.set_moving_speed(500)

angle1 = 0
angle2 = 0

while True:
    input_pos = int(input("goal pos: "))
    my_dxl1.set_moving_speed(200)
    my_dxl1.set_ccw_angle_limit(input_pos)
