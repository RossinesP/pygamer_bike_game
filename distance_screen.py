from screen import Screen
from tracker import Tracker

from adafruit_display_text import label
import neopixel
import terminalio

class DistanceScreen(Screen):

    def __init__(self, screen_manager, pixels: neopixel.NeoPixel, tracker: Tracker, initial_distance=0.0):
        super().__init__(screen_manager, pixels, tracker)
        font = terminalio.FONT
        color = 0xFFFFFF
        self.dst_label = label.Label(font, text="0.00", color=color, scale= 5)
        self.dst_label.x = 25
        self.dst_label.y = 50
        self.dst_label.anchor_point = (1,0)
        self.dst_label.text = self.get_distance_text(initial_distance)

        self.dst_unit_label = label.Label(font, text="km", color=color, scale=2)
        self.dst_unit_label.x = 70
        self.dst_unit_label.y = 100

        self.group.append(self.dst_label)
        self.group.append(self.dst_unit_label)

    def get_distance_text(self, distance: float):
        if distance >= 1000000:
            return "FAR"
        elif distance >= 100000:
            dst_km = distance / 1000.0
            return f"{dst_km:04.0f}"
        elif distance >= 10000:
            dst_km = distance / 1000.0
            return f"{dst_km:04.1f}"
        elif distance >= 500:
            dst_km = distance / 1000.0
            return f"{dst_km:04.2f}"
        elif distance >= 100:
            return f"{distance:.0f}"
        else:
            return f"{distance:.0f}"

    def get_distance_unit_text(self, distance: float):
        if distance >= 500:
            return "km"
        else:
            return "m"

    def on_tracker_update(self, now: int):
        distance = self.tracker.get_distance()
        self.dst_label.text = self.get_distance_text(distance)
        self.dst_unit_label.text = self.get_distance_unit_text(distance)