from screen import Screen
from tracker import Tracker

from adafruit_display_text import label
import neopixel
import terminalio

class DurationScreen(Screen):

    def __init__(self, screen_manager, pixels: neopixel.NeoPixel, tracker: Tracker, now:int):
        super().__init__(screen_manager, pixels, tracker)
        font = terminalio.FONT
        color = 0xFFFFFF
        self.time_label = label.Label(font, text="00:00:00", color=color, scale= 3)
        self.time_label.x = 10
        self.time_label.y = 60
        self.time_label.anchor_point = (1,0)

        self.group.append(self.time_label)

    def get_time_text(self, duration: int):
        # Beware, duration can be None before the first tick
        if duration:
            # To avoid the length of the string to exceed the allocated length,
            # we reset the hours after 99h.
            # Champions who'd like to break a record are welcome to improve this
            # part.
            hours = (duration / 3600) % 99
            minutes = (duration / 60) % 60
            seconds = duration % 60
            return f"{hours:02.0f}:{minutes:02.0f}:{seconds:02.0f}"
        else:
            return "--:--:--"

    def on_tracker_update(self, now: int):
        duration = self.tracker.get_duration(now)
        self.time_label.text = self.get_time_text(duration)