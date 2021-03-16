import board
import neopixel
import time
from digitalio import DigitalInOut, Direction, Pull
import ugame
from adafruit_display_text import label

from tracker import Tracker
from screen_manager import ScreenManager
import gc

########################
# Neopixel setup
########################
pixel_pin = board.NEOPIXEL
NUM_PIXELS = 5

PIXELS_ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin,
    NUM_PIXELS,
    brightness=0.2,
    auto_write=False,
    pixel_order=PIXELS_ORDER
)

#######################
# REED setup
#######################
reed = DigitalInOut(board.D2)
reed.direction = Direction.INPUT
reed.pull = Pull.UP

reed_previous_value = False


#######################
# Stats tracking
#######################
tracker = Tracker()

#######################
# Display Setup
#######################
display = board.DISPLAY

screen_mgr = ScreenManager(display, pixels, tracker)

######################
# Main loop
######################

display.auto_refresh = False

i = 0
while True:
    # Get the time
    now = time.monotonic()

    cur_btn_vals = ugame.buttons.get_pressed()

    # Read the buttons value
    a_btn_value = cur_btn_vals & ugame.K_O
    b_btn_value = cur_btn_vals & ugame.K_X
    up_btn_value = cur_btn_vals & ugame.K_UP
    down_btn_value = cur_btn_vals & ugame.K_DOWN
    start_btn_value = cur_btn_vals & ugame.K_START
    select_btn_value = cur_btn_vals & ugame.K_SELECT

    # For debug purposes, we also read the A button value to simulate
    # the reed switch
    reed_value = not reed.value or (a_btn_value > 0)

    if b_btn_value:
        screen_mgr.on_b(now)
    if up_btn_value:
        screen_mgr.on_joystick_up(now)
    if down_btn_value:
        screen_mgr.on_joystick_down(now)
    if start_btn_value:
        screen_mgr.on_start(now)

    # Check if the reed value has changed
    # (e.g. if the wheel has completed a full rotation)
    has_reed_closed = reed_value and not reed_previous_value
    if has_reed_closed:
        print(f"closed {i}")
        i += 1
    reed_previous_value = reed_value

    if has_reed_closed:
        tracker.on_tick(now)


    screen_mgr.on_tracker_update(now)
    display.refresh()

    # print(f"Free memory : {gc.mem_free()}")

    time.sleep(0.01) # debounce delay