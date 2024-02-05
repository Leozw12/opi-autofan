import os
import time
from datetime import datetime

import wiringpi
from wiringpi import GPIO


GPIO_OUT = 17
START_TEMP = 50
STOP_TEMP = 40
DELAY_TIME = 10


def get_cpu_temperature():
    base_dir = '/sys/class/thermal/'
    for thermal_zone in os.listdir(base_dir):
        if thermal_zone.startswith('thermal_zone'):
            with open(os.path.join(base_dir, thermal_zone, 'type'), 'r') as f:
                if 'cpu' in f.read().lower():
                    with open(os.path.join(base_dir, thermal_zone, 'temp'), 'r') as f_temp:
                        temperature = float(f_temp.read()) / 1000
                        return temperature
    return None


def open_fan():
    wiringpi.digitalWrite(GPIO_OUT, GPIO.LOW)


def close_fan():
    wiringpi.digitalWrite(GPIO_OUT, GPIO.HIGH)


def init_gpio():
    wiringpi.wiringPiSetup()
    wiringpi.pinMode(GPIO_OUT, wiringpi.OUTPUT)
    wiringpi.digitalWrite(GPIO_OUT, GPIO.HIGH)
    print('Init fan mode.')


def main():
    init_gpio()
    status = False

    try:
        while True:
            temp = get_cpu_temperature()

            if temp >= START_TEMP and not status:
                open_fan()
                status = True
                print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - Current temperature is {temp}℃ / open fan')
            elif temp <= STOP_TEMP and status:
                close_fan()
                status = False
                print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - Current temperature is {temp}℃ / close fan')

            time.sleep(DELAY_TIME)
    except Exception as e:
        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - {e}')
        GPIO.cleanup()


if __name__ == "__main__":
    main()
