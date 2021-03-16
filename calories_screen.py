from screen import Screen
from tracker import Tracker

from adafruit_display_text import label
import neopixel
import terminalio

class CaloriesScreen(Screen):

    def __init__(self, screen_manager, pixels: neopixel.NeoPixel, tracker: Tracker):
        super().__init__(screen_manager, pixels, tracker)
        font = terminalio.FONT
        color = 0xFFFFFF
        self.cal_label = label.Label(font, text="0.00", color=color, scale= 5)
        self.cal_label.x = 25
        self.cal_label.y = 50
        self.cal_label.anchor_point = (1,0)
        self.cal_label.text = self.get_calories_text(tracker.calories)

        self.cal_unit_label = label.Label(font, text="km", color=color, scale=2)
        self.cal_unit_label.x = 70
        self.cal_unit_label.y = 100
        self.cal_unit_label.text = "cal"

        self.group.append(self.cal_label)
        self.group.append(self.cal_unit_label)

    def get_calories_text(self, calories: float):
        if calories >= 10000:
            return "LOTS"
        else:
            return f"{calories:.0f}"

    def on_tracker_update(self, now: int):
        self.cal_label.text = self.get_calories_text(self.tracker.calories)