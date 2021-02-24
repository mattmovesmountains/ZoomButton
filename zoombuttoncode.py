"""Zoom On Air Button - V1.0 - Chromebook/Linux"""


import time
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
import adafruit_dotstar as dotstar

# Define our LED
dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
dot.brightness = 0.3


red = (255,0,0)
green = (0,255,0)
silver = (216, 216, 216)
colors = [red,green,silver]


mute_count = 0

# The pins we'll use, each will have an internal pullup; using just one pin here 'D0'
keypress_pins = [board.D0]
# Our array of key objects (only useful if I changed code to have more pins)
key_pin_array = []
# The Keycode sent for each button, will be paired with a control key
control_key1 = Keycode.ALT
#control_key2 = Keycode.SHIFT    (needed only for mac)
mykey = Keycode.A

# The keyboard object!
time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)  # We're in the US :)

# A bit unnecessary for just one pin, but here for reference
# Make all pin objects inputs with pullups
for pin in keypress_pins:
    key_pin = digitalio.DigitalInOut(pin)
    key_pin.direction = digitalio.Direction.INPUT
    key_pin.pull = digitalio.Pull.UP
    key_pin_array.append(key_pin)

# Just some lighting stuff
# For most CircuitPython boards:
led = digitalio.DigitalInOut(board.D13)
# For QT Py M0:
# led = digitalio.DigitalInOut(board.SCK)
led.direction = digitalio.Direction.OUTPUT

print("Waiting for key pin...")

# Cycle through colors when called
def xmas_fade(color_list):

    for color in colors:
        dot.brightness = 0.1

        for i in range(0,8):
            dot.brightness += 0.1
            dot[0] = color
            time.sleep(0.05)
            time.sleep(3)

        for i in range(0,8):
            dot.brightness -= 0.1
            dot[0] = color
            time.sleep(0.03)
        time.sleep(0.25)
    dot.brightness = 0.7
    dot[0] = red


while True:

    # Check each pin
    for key_pin in key_pin_array: # Should just be one: D0
        if not key_pin.value:  # Is it grounded?
            i = key_pin_array.index(key_pin)
            print("Pin #%d is grounded." % i)

            # Turn on the red LED
            led.value = True

            while not key_pin.value:
                pass  # Wait for it to be ungrounded!
            # "Type" the Keycode or string

            keyboard.press(control_key1, mykey)  # "Press"...
            keyboard.release_all()  # ..."Release"!
            mute_count += 1
            if mute_count%2 != 0:
                dot.brightness = 0.7
                dot[0] = red
            else:
                dot.brightness = 0.1
                dot[0] = green


            # Turn off the red LED
            led.value = False

    time.sleep(0.01)