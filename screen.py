import displayio
import neopixel

class Screen():

    def __init__(self, screen_manager, pixels, tracker):
        self.screen_manager = screen_manager
        self.group_size = 10
        self.group = displayio.Group(max_size=self.group_size)
        self.tracker = tracker
        self.pixels = pixels

        for i in range(len(pixels)):
            pixels[i] = (0, 0, 0)
        pixels.show()

    def clear_group(self):
        while len(self.group) != 0:
            del self.group[0]

    def on_tracker_update(self, now: int):
        return False

    def on_joystick_up(self, now:int):
        return False

    def on_joystick_down(self, now:int):
        return False

    def on_start(self, now:int):
        return False

    def on_select(self, now:int):
        return False

    def on_b(self, now:int):
        return False