from screen import Screen
from tracker import Tracker

from adafruit_display_text import label
import displayio
import math
import neopixel
import terminalio

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 128
BITMAP_WIDTH = 80
BITMAP_HEIGHT = 20

class SpeedScreen(Screen):

    def __init__(self, screen_manager, pixels: neopixel.NeoPixel, tracker: Tracker, initial_speed=0.0):
        super().__init__(screen_manager, pixels, tracker)
        font = terminalio.FONT
        color = 0xFFFFFF
        self.speed_label = label.Label(font, text="0.00", color=color, scale= 5)
        self.speed_label.x = 10
        self.speed_label.y = 45
        self.speed_label.text = self.get_speed_text(initial_speed)

        self.speed_unit_label = label.Label(font, text="km/h", color=color, scale=1)
        self.speed_unit_label.x = 135
        self.speed_unit_label.y = 65

        self.group.append(self.speed_label)
        self.group.append(self.speed_unit_label)

        bitmap, tile_grid = self.get_bitmap()
        self.graph_bitmap = bitmap
        self.group.append(tile_grid)

        self.previous_screen_update_time = 0

    def get_bitmap(self):
        bitmap = displayio.Bitmap(BITMAP_WIDTH, BITMAP_HEIGHT, 2)
        palette = displayio.Palette(2)
        palette[0] = 0x000000
        palette[1] = 0xFFFFFF
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
        tile_grid.x = int((SCREEN_WIDTH - BITMAP_WIDTH) / 2)
        tile_grid.y = int(SCREEN_HEIGHT - BITMAP_HEIGHT - 10)

        return (bitmap, tile_grid)


    def set_led_colors(self, average_speed:float, max_speed:float):
        '''
        Sets the LED colors depending on the speed.
        The leds will go from green to red.
        The lights indicate the % or the max speed that the user
        is going right now.
        '''
        dim_factor = 0.2
        # if self.tracker.max_speed == 0:
        if max_speed == 0:
            max_pixel_to_light = 5
        else:
            # max_pixel_to_light = math.ceil(6 * (average_speed / self.tracker.max_speed)) - 1
            max_pixel_to_light = math.ceil(6 * (average_speed / max_speed)) - 1
        for i in range(len(self.pixels)):
            if i >= max_pixel_to_light:
                color = (0, 0, 0)
            elif i < 2:
                color = (0, int(255*dim_factor), 0)  # Green
            elif i < 4:
                color = (int(255*dim_factor), int(165*dim_factor), 0) # Orange
            else:
                color = (int(255*dim_factor), 0, 0) # Red
            self.pixels[i] = color
        self.pixels.show()

    def get_speed_text(self, speed: float):
        if speed >= 1000:
            return "FAST"
        elif speed >= 100:
            return f"{speed:04.0f}"
        else:
            return f"{speed:04.1f}"

    def on_tracker_update(self, now: int):
        # TODO : improve this, as right now one
        # pixel = one speed value over the time
        # during a full wheel rotation,
        # which means the graph won't be updated
        # if the user stops pedalling

        super().on_tracker_update(now)
        speed = self.tracker.get_avg_speed(now)
        self.speed_label.text = self.get_speed_text(speed)


        if now - self.previous_screen_update_time >= 1:
            # retrieve the max speed
            speeds = []
            previous_ticks_length = len(self.tracker.previous_ticks)
            if previous_ticks_length < 2:
                return

            max_speed = 0
            for tick_index in range(1, previous_ticks_length):
                curr_tick = self.tracker.previous_ticks[tick_index]
                prev_tick = self.tracker.previous_ticks[tick_index - 1]

                curr_speed = self.tracker.get_speed(1, curr_tick - prev_tick)
                speeds.append(curr_speed)
                if curr_speed > max_speed:
                    max_speed = curr_speed

            self.set_led_colors(speed, max_speed)

            self.previous_screen_update_time = now

            previous_speeds_length = len(speeds)
            for i in range(previous_speeds_length):
                previous_speed = speeds[previous_speeds_length - 1 - i]
                if max_speed:
                    percent_max = int(previous_speed / max_speed * BITMAP_HEIGHT)
                else:
                    percent_max = 0
                for j in range(percent_max):
                    self.graph_bitmap[BITMAP_WIDTH - 1 - i, BITMAP_HEIGHT - 1 - j] = 1
                for j in range(BITMAP_HEIGHT - percent_max):
                    self.graph_bitmap[BITMAP_WIDTH - 1 - i, j] = 0