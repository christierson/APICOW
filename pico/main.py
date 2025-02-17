from api import API
from board import Board
from machine import Pin
from utime import sleep

led = Pin(0, Pin.OUT)
def blink():
    led.value(1)
    sleep(0.5)
    led.value(0)

blink()

board = Board()
sleep(0.5)
blink()
sleep(0.5)
api = API(board.recieve)
sleep(0.5)
blink()
sleep(0.5)
api.run()
