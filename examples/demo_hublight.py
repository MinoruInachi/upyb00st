from upyb00st import *
from utime import sleep

MY_MOVEHUB_ADD = b'\x00\x16\x53\xA9\xE5\x86'
mymovehub = MoveHub(MY_MOVEHUB_ADD)

def blink_light(color):
    for i in range(3):
        mymovehub.set_hublight(color)
        sleep(0.5)
        mymovehub.set_hublight('OFF')
        sleep(0.5)

try:
    mymovehub.start()

    for color in LED_COLORS[1:]:
        blink_light(color)

finally:
    mymovehub.stop()
