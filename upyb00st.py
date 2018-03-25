#
# WiPy 2.0 MicroPython API for LEGO BOOST.
#

from network import Bluetooth
from utime import sleep_ms
from micropython import const

PORT_A = const(0x37)
PORT_B = const(0x38)
PORT_C = const(0x01)
PORT_D = const(0x02)
PORT_TILT = const(0x3A)

TYPE_NONE = const(0x00)
TYPE_LED = const(0x17)
TYPE_COLORDISTANCE = const(0x25)
TYPE_ENCODERMOTOR = const(0x26)
TYPE_MOTOR = const(0x27)
TYPE_HUBTILT = const(0x28)

SET_LED_INI = b'\x08\x00\x81\x32\x11\x51\x00'

LED_COLORS = ['OFF', 'PINK', 'PURPLE', 'BLUE', 'LIGHTBLUE',
 'CYAN', 'GREEN', 'YELLOW', 'ORANGE', 'RED', 'WHITE']

MOTOR_A = b'\x37'
MOTOR_B = b'\x38'
MOTOR_AB = b'\x39'
MOTOR_C = b'\x01'
MOTOR_D = b'\x02'

MOTORS = [MOTOR_A, MOTOR_B, MOTOR_AB, MOTOR_C, MOTOR_D]

MOTOR_PAIRS = [MOTOR_AB]

MOTOR_TIMED_INI = b'\x0c\x01\x81'
MOTOR_TIMED_MID = b'\x11\x09'
MOTOR_TIMED_END = b'\x64\x7f\x03'

MOTORS_TIMED_INI = b'\x0d\x01\x81'
MOTORS_TIMED_MID = b'\x11\x0A'
MOTORS_TIMED_END = b'\x64\x7f\x03'

MOTOR_ANGLE_INI = b'\x0e\x01\x81'
MOTOR_ANGLE_MID = b'\x11\x0b'
MOTOR_ANGLE_END = b'\x64\x7f\x03'

MOTORS_ANGLE_INI = b'\x0f\x01\x81'
MOTORS_ANGLE_MID = b'\x11\x0c'
MOTORS_ANGLE_END = b'\x64\x7f\x03'

LISTEN_INI = b'\x0a\x00\x41'
LISTEN_END = b'\x01\x00\x00\x00\x01'
LISTEN_BUTTON = b'\x05\x00\x01\x02\x02'

MODE_COLORDIST_SENSOR = b'\x08'
MODE_ENCODER = b'\x02'
MODE_HUBTILT_BASIC = b'\x02'
MODE_HUBTILT_FULL = b'\x00'

COLOR_SENSOR_COLORS = ['BLACK', '', '', 'BLUE', '', 'GREEN',
 '', 'YELLOW', '', 'RED', 'WHITE']

ENCODER_MID = 2147483648
ENCODER_MAX = 4294967296

BUTTON_PRESSED = '\x01'
BUTTON_RELEASED = '\x00'

TILT_HORIZ = const(0x00)
TILT_UP = const(0x01)
TILT_DOWN = const(0x02)
TILT_RIGHT = const(0x03)
TILT_LEFT = const(0x04)
TILT_INVERT = const(0x05)

TILT_BASIC_TEXT = ['TILT_HORIZ', 'TILT_UP', 'TILT_DOWN',
                   'TILT_RIGHT', 'TILT_LEFT', 'TILT_INVERT', '']

class MoveHub (object):
    def __init__(self, address):
        self.address = address
        self.conn = None
        self.last_color_C = ''
        self.last_color_D = ''
        self.last_distance_C = ''
        self.last_distance_D = ''
        self.last_brightness_C = 0
        self.last_brightness_D = 0
        self.last_angle_A = ''
        self.last_angle_B = ''
        self.last_angle_C = ''
        self.last_angle_D = ''
        self.last_angle_AB = ''
        self.last_button = ''
        self.last_hubtilt = 6
        self.devicename = ''
        self.wqueue = []
        self.is_subscribe = False

    def start(self):
        self.ble = Bluetooth()
        self.conn = self.ble.connect(self.address)
        while not self.conn.isconnected():
            sleep_ms(100)
        sleep_ms(2000)
        self.svcs = self.conn.services()
        self.chars = self.svcs[2].characteristics()
        self.devicename = self.svcs[1].characteristics()[0].read().decode('utf-8')

    def stop(self):
        if self.conn is not None:
            if self.conn.isconnected():
                self.conn.disconnect()
            self.conn = None

    def is_connected(self):
        if self.conn is not None:
            return self.conn.isconnected()
        return False

    def gat_address(self):
        return self.address

    def get_name(self):
        return self.devicename

    def set_hublight(self, color):
        command = SET_LED_INI
        command += bytes([LED_COLORS.index(color)])
        self._write(command)

    def run_motor_for_time(self, motor, time_ms, dutycycle_pct):
        if motor in MOTORS:
            if dutycycle_pct in range(-100, 101):
                command = MOTOR_TIMED_INI
                command += motor
                command += MOTOR_TIMED_MID
                t = bytes((time_ms & 0xff, (time_ms >> 8) & 0xff))
                command += t
                if dutycycle_pct < 0:
                    dutycycle_pct += 255
                command += bytes([dutycycle_pct])
                command += MOTOR_TIMED_END
                self._write(command)

    def run_motors_for_time(self, motor, time_ms,
                            dutycycle_pct_a, dutycycle_pct_b):
        if motor in MOTOR_PAIRS:
            if (dutycycle_pct_a in range(-100, 101) and
                dutycycle_pct_b in range(-100, 101)):
                command = MOTORS_TIMED_INI
                command += motor
                command += MOTORS_TIMED_MID
                t = bytes((time_ms & 0xff, (time_ms >> 8) & 0xff))
                command += t
                if dutycycle_pct_a < 0:
                    dutycycle_pct_a += 255
                command += bytes([dutycycle_pct_a])
                if dutycycle_pct_b < 0:
                    dutycycle_pct_b += 255
                command += bytes([dutycycle_pct_b])
                command += MOTORS_TIMED_END
                self._write(command)

    def run_motor_for_angle(self, motor, angle, dutycycle_pct):
        if motor in MOTORS:
            if dutycycle_pct in range(-100, 101):
                command = MOTOR_ANGLE_INI
                command += motor
                command += MOTOR_ANGLE_MID
                ang = bytes((angle & 0xff, (angle >> 8) & 0xff,
                             (angle >> 16) & 0xff, (angle >> 24) & 0xff))
                command += ang
                if dutycycle_pct < 0:
                    dutycycle_pct += 255
                command += bytes([dutycycle_pct])
                command += MOTOR_ANGLE_END
                self._write(command)

    def run_motors_for_angle(self, motor, angle, dutycycle_pct_a,
                             dutycycle_pct_b):
        if motor in MOTORS:
            if (dutycycle_pct_a in range(-100, 101) and
                dutycycle_pct_b in range(-100, 101)):
                command = MOTORS_ANGLE_INI
                command += motor
                command += MOTORS_ANGLE_MID
                ang = bytes((angle & 0xff, (angle >> 8) & 0xff,
                             (angle >> 16) & 0xff, (angle >> 24) & 0xff))
                command += ang
                if dutycycle_pct_a < 0:
                    dutycycle_pct_a += 255
                command += bytes([dutycycle_pct_a])
                if dutycycle_pct_b < 0:
                    dutycycle_pct_b += 255
                command += bytes([dutycycle_pct_b])
                command += MOTORS_ANGLE_END
                self._write(command)

    @staticmethod
    def parse_notifications(self):
        if len(self.wqueue) > 0:
            command = self.wqueue.pop(0)
            self.chars[0].write(command)
        value = self.chars[0].read()
        if value is None or len(value) < 5:
            return
        #bstr = ''
        #for i in range(len(value)):
        #    bstr += hex(value[i]) + ' '
        #print('value:', bstr)
        if value[0] == 0x08 and value[1] == 0x00 and value[2] == 0x45:
            if value[3] == PORT_A:
                self.last_angle_A = (value[4] + value[5] * 256 +
                                     value[6] * 65536 +
                                     value[7] * 16777216)
                if self.last_angle_A > ENCODER_MID:
                    self.last_angle_A = self.last_angle_A - ENCODER_MAX
            elif value[3] == PORT_B:
                self.last_angle_B = (value[4] + value[5] * 256 +
                                     value[6] * 65536 +
                                     value[7] * 16777216)
                if self.last_angle_B > ENCODER_MID:
                    self.last_angle_B = self.last_angle_B - ENCODER_MAX
            elif value[3] == PORT_C:
                if self._port_C_is == TYPE_COLORDISTANCE:
                    if value[4] != 0xFF:
                        self.last_color_C = COLOR_SENSOR_COLORS[value[4]]
                        self.last_brightness_C = value[7]
                        self.last_distance_C = ''
                    else:
                        self.last_color_C = ''
                        self.last_brightness_C = 0
                        self.last_distance_C = value[5]
                elif self._port_C_is == TYPE_ENCODERMOTOR:
                    self.last_angle_C = (value[4] + value[5] * 256 +
                                         value[6] * 65536 +
                                         value[7] * 16777216)
                    if self.last_angle_C > ENCODER_MID:
                        self.last_angle_C = (self.last_angle_C -
                                             ENCODER_MAX)
            elif value[3] == PORT_D:
                if self._port_D_is == TYPE_COLORDISTANCE:
                    if value[4] != 0xFF:
                        self.last_color_D = COLOR_SENSOR_COLORS[value[4]]
                        self.last_brightness_D = value[7]
                        self.last_distance_D = ''
                    else:
                        self.last_color_D = ''
                        self.last_brightness_D = 0
                        self.last_distance_D = value[5]
                elif self._port_D_is == TYPE_ENCODERMOTOR:
                    self.last_angle_D = (value[4] +
                                         value[5]*256 +
                                         value[6]*65536 +
                                         value[7]*16777216)
                    if self.last_angle_D > ENCODER_MID:
                        self.last_angle_D = (self.last_angle_D -
                                             ENCODER_MAX)
            elif value[3] == MOTOR_AB:
                pass
        elif (value[0] == 0x06 and value[1] == 0x00 and
              value[2] == 0x01 and value[3] == 0x02 and
              value[4] == 0x06):
            if value[5] == 1:
                self.last_button = BUTTON_PRESSED
            elif value[5] == 0:
                self.last_button = BUTTON_RELEASED
            else:
                self.last_button = ''
        elif (value[0] == 0x05 and value[1] == 0x00 and
              value[2] == 0x45 and value[3] == 0x3a):
            if value[4] in range(6):
                self.last_hubtilt = value[4]
            else:
                self.last_hubtilt = 6
                print('Tilt: Unknown value')

    def subscribe_all(self):
        self.chars[0].callback(Bluetooth.CHAR_NOTIFY_EVENT, MoveHub.parse_notifications, self)
        self.is_subscribe = True

    def listen_colordist_sensor(self, port):
        if port in [PORT_C, PORT_D]:
            command = LISTEN_INI
            command += bytes([port])
            command += MODE_COLORDIST_SENSOR
            command += LISTEN_END
            if port == PORT_C:
                self._port_C_is = TYPE_COLORDISTANCE
            else:
                self._port_D_is = TYPE_COLORDISTANCE
            self.chars[0].write(command)

    def listen_angle_sensor(self, port):
        if port in [PORT_A, PORT_B, PORT_C, PORT_D]:
            command = LISTEN_INI
            command += bytes([port])
            command += MODE_ENCODER
            command += LISTEN_END
            if port == PORT_C:
                self._port_C_is = TYPE_ENCODERMOTOR
            elif port == PORT_D:
                self._port_D_is = TYPE_ENCODERMOTOR
            self.chars[0].write(command)

    def listen_button(self):
        self.chars[0].write(LISTEN_BUTTON)

    def listen_hubtilt(self, mode):
        if mode in [MODE_HUBTILT_BASIC, MODE_HUBTILT_FULL]:
            command = LISTEN_INI
            command += bytes([PORT_TILT])
            command += mode
            command += LISTEN_END
            self.chars[0].write(command)

    def _write(self, command):
        if self.is_subscribe:
            self.wqueue.append(command)
        else:
            self.chars[0].write(command)
