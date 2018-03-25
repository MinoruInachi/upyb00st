from upyb00st import *
from utime import sleep

MY_MOVEHUB_ADD = b'\x00\x16\x53\xA9\xE5\x86'
mymovehub = MoveHub(MY_MOVEHUB_ADD)

try:
    print('connect MH')
    mymovehub.start()

    mymovehub.listen_hubtilt(MODE_HUBTILT_BASIC)
    mymovehub.subscribe_all()

    while True:
        sleep(0.2)
        print(TILT_BASIC_TEXT[mymovehub.last_hubtilt])

finally:
    mymovehub.stop()
