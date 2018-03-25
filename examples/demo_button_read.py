from upyb00st import *
from utime import sleep

MY_MOVEHUB_ADD = b'\x00\x16\x53\xA9\xE5\x86'
mymovehub = MoveHub(MY_MOVEHUB_ADD)

try:
    mymovehub.start()

    mymovehub.listen_button()
    mymovehub.subscribe_all()

    while True:
        sleep(0.2)
        if mymovehub.last_button == BUTTON_PRESSED:
            print('PRESSED')
        elif mymovehub.last_button == BUTTON_RELEASED:
            print('RELEASED')
        else:
            print('UNKNOWN')

finally:
    mymovehub.stop()
