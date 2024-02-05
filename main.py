import time
from datetime import datetime

import wiringpi
from wiringpi import GPIO


GPIO_OUT = 17
START_TEMP = 55
STOP_TEMP = 40
DELAY_TIME = 15


def get_cpu_temperature():
    with open("/sys/class/thermal/thermal_zone0/temp", 'r') as f:
        temperature = float(f.read()) / 1000
    return temperature


def open_fan():
    wiringpi.digitalWrite(GPIO_OUT, GPIO.LOW)


def close_fan():
    wiringpi.digitalWrite(GPIO_OUT, GPIO.HIGH)


def init_gpio():
    wiringpi.wiringPiSetup()
    wiringpi.pinMode(GPIO_OUT, wiringpi.OUTPUT)
    wiringpi.digitalWrite(GPIO_OUT, GPIO.HIGH)


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
