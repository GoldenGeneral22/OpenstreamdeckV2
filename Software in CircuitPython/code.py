#importing relevant libraries
import time
import board
import digitalio
import rotaryio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from  adafruit_hid.consumer_control_code import  ConsumerControlCode

# Custom "Enum" class replacement for CircuitPython
class Keys:
    _members = {
        'Null': 0,
        'F13': 1,
        'F14': 2,
        'F15': 3,
        'F16': 4,
        'F17': 5,
        'F18': 6,
        'Mute': 7,
        'Vol_Decrease': 8,
        'Vol_Increase': 9,
    }
    @classmethod
    def get_by_value(cls, value):
        for name, val in cls._members.items():
            if val == value:
                return name
        return None
    @classmethod
    def get_value(cls, name):
        return cls._members.get(name, None)
    @classmethod
    def items(cls):
        return cls._members.items()

# Definition of pins for RPI Pico clone
inputLed = digitalio.DigitalInOut(board.GP25)
inputLed.direction = digitalio.Direction.OUTPUT

outputLanes = [digitalio.DigitalInOut(board.GP15), digitalio.DigitalInOut(board.GP14)]
for lane in outputLanes:
    lane.direction = digitalio.Direction.OUTPUT

detectLanes = [digitalio.DigitalInOut(board.GP6), digitalio.DigitalInOut(board.GP7), digitalio.DigitalInOut(board.GP8)]
for lane in detectLanes:
    lane.direction = digitalio.Direction.INPUT
    lane.pull = digitalio.Pull.UP

# Definition of relevant variaboardles, etc.
kbd = Keyboard(usb_hid.devices)
inputLedDelay = 0.05
rows = 2
columns = 3

# setup() runs once at startup
def setup():
    ledBurst()
    time.sleep(inputLedDelay)
    ledBurst()
    time.sleep(inputLedDelay)
    ledBurst()

# ledBurst() lets the inputLed blink once
def ledBurst() -> None:
    inputLed.value = True
    time.sleep(inputLedDelay)
    inputLed.value = False

# checkForInput() is repeated infinitely by the main loop
def checkForInput():
    for row in outputLanes:
        row.value = True
        for colum in detectLanes:
            if not colum.value:
                enum_value = outputLanes.index(row) * 3 + detectLanes.index(colum) + 1
                return Keys.get_by_value(enum_value)
        row.value = False
    return 'Null'

# processInput() sends the Keycode to the Computer
def processInput(input):
    if input == 'F13':
        kbd.send(Keycode.F13)
    elif input == 'F14':
        kbd.send(Keycode.F14)
    elif input == 'F15':
        kbd.send(Keycode.F15)
    elif input == 'F16':
        kbd.send(Keycode.F16)
    elif input == 'F17':
        kbd.send(Keycode.F17)
    elif input == 'F18':
        kbd.send(Keycode.F18)
    else:
        return

# loop() runs as long as the microcontroller has power
def loop():
    activeButton = None
    while True:
        input = checkForInput()
        if input != 'Null' and activeButton is None:
            activeButton = input
            print(input)
            processInput(input)
            ledBurst()
        elif input == 'Null' and activeButton is not None:
            activeButton = None

# main() is the program's main thread
def main():
    setup()
    loop()    
main()