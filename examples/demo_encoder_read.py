from upyb00st import *
from utime import sleep

MY_MOVEHUB_ADD = b'\x00\x16\x53\xA9\xE5\x86'
mymovehub = MoveHub(MY_MOVEHUB_ADD)

try:
    mymovehub.start()

    mymovehub.listen_angle_sensor(PORT_D)
    mymovehub.subscribe_all()

    while True:
        sleep(0.2)
        print(mymovehub.last_angle_D)

finally:
    mymovehub.stop()
