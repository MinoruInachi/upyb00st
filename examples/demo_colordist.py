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
        print('Color: {}, Distance: {}, Brightness {}'.format(mymovehub.last_color_C,
                                                              mymovehub.last_distance_C,
                                                              mymovehub.last_brightness_C))

finally:
    mymovehub.stop()
