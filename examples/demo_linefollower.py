from upyb00st import *
from utime import sleep

MY_MOVEHUB_ADD = b'\x00\x16\x53\xA9\xE5\x86'
mymovehub = MoveHub(MY_MOVEHUB_ADD)

try:
    mymovehub.start()
    mymovehub.listen_colordist_sensor(PORT_C)
    mymovehub.subscribe_all()

    while True:
        sleep(0.2)
        if mymovehub.last_brightness_C >= 6:
            mymovehub.run_motors_for_time(MOTOR_AB, 200, 100, 5)
        else:
            mymovehub.run_motors_for_time(MOTOR_AB, 200, 5, 100)

finally:
    mymovehub.stop()
