from upyb00st import *
from utime import sleep

MY_MOVEHUB_ADD = b'\x00\x16\x53\xA9\xE5\x86'
mymovehub = MoveHub(MY_MOVEHUB_ADD)

try:
    mymovehub.start()

    # turn motor A ON for 1000 ms at 100% duty cycle in both directions
    mymovehub.run_motor_for_time(MOTOR_A, 1000, 100)
    sleep(1)
    mymovehub.run_motor_for_time(MOTOR_A, 1000, -100)
    sleep(1)

    sleep(0.5)

    # rotate motor 90 degrees at 100% duty cycle in both directions
    mymovehub.run_motor_for_angle(MOTOR_A, 90, 100)
    sleep(0.5)
    mymovehub.run_motor_for_angle(MOTOR_A, 90, -100)

    sleep(0.5)

    # turn pair AB ON for 1000 ms at 100% duty cycle in both direction
    mymovehub.run_motors_for_time(MOTOR_AB, 1000, 100, 100)
    sleep(1)
    mymovehub.run_motors_for_time(MOTOR_AB, 1000, 100, -100)
    sleep(1)
    mymovehub.run_motors_for_time(MOTOR_AB, 1000, -100, -100)
    sleep(1)
    mymovehub.run_motors_for_time(MOTOR_AB, 1000, -100, 100)
    sleep(1)

    sleep(0.5)

    # rotate pair AB 90 degrees at 100% duty cycle in both direction
    mymovehub.run_motors_for_angle(MOTOR_AB, 90, 100, 100)
    sleep(0.5)
    mymovehub.run_motors_for_angle(MOTOR_AB, 90, 100, -100)
    sleep(0.5)
    mymovehub.run_motors_for_angle(MOTOR_AB, 90, -100, -100)
    sleep(0.5)
    mymovehub.run_motors_for_angle(MOTOR_AB, 90, -100, 100)
    sleep(0.5)

finally:
    mymovehub.stop()
