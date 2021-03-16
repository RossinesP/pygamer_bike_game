from speed_screen import SpeedScreen
from distance_screen import DistanceScreen
from calories_screen import CaloriesScreen
from duration_screen import DurationScreen
from game_screen import TimeSelectionScreen, OngoingGameScreen

import time

SCREEN_SPEED = 0
SCREEN_DISTANCE = 1
SCREEN_CALORIES = 2
SCREEN_TIME = 3
SCREEN_GAME_TIME_SELECT = 4
SCREEN_GAME_ONGOING = 5

class ScreenManager():
    SCREENS = [
        SCREEN_GAME_TIME_SELECT,
        SCREEN_SPEED,
        SCREEN_DISTANCE,
        SCREEN_CALORIES,
        SCREEN_TIME,

    ]

    def __init__(self, display, pixels: neopixel.NeoPixel, tracker):
        self.display = display
        self.pixels = pixels
        self.tracker = tracker
        self.last_b_time = 0
        self.set_screen(self.SCREENS[0])

    def set_ongoing_screen(self, now: int, duration: int):
        screen = OngoingGameScreen(self, self.pixels, self.tracker, now, duration)
        screen_id = SCREEN_GAME_ONGOING
        self.display.show(screen.group)
        self.current_screen_id = screen_id
        self.current_screen = screen

    def set_screen(self, new_screen_id: int):
        if new_screen_id == SCREEN_DISTANCE:
            screen = DistanceScreen(self, self.pixels, self.tracker, 0.0)
            screen_id = SCREEN_DISTANCE
        elif new_screen_id == SCREEN_CALORIES:
            screen = CaloriesScreen(self, self.pixels, self.tracker)
            screen_id = SCREEN_CALORIES
        elif new_screen_id == SCREEN_TIME:
            screen = DurationScreen(self, self.pixels, self.tracker, time.monotonic())
            screen_id = SCREEN_TIME
        elif new_screen_id == SCREEN_GAME_TIME_SELECT:
            screen = TimeSelectionScreen(self, self.pixels, self.tracker)
            screen_id = SCREEN_GAME_TIME_SELECT
        else:
            # Speed screen by default
            screen = SpeedScreen(self, self.pixels, self.tracker, 0.0)
            screen_id = SCREEN_SPEED

        self.display.show(screen.group)
        self.current_screen_id = new_screen_id
        self.current_screen = screen

    def cycle_screens(self):
        if self.current_screen_id in self.SCREENS:
            next_screen_id = (self.current_screen_id + 1) % len(self.SCREENS)
        else:
            next_screen_id = self.SCREENS[0]
        self.set_screen(next_screen_id)

    def on_tracker_update(self, now: int):
        self.current_screen.on_tracker_update(now)

    def on_joystick_up(self, now:int):
        self.current_screen.on_joystick_up(now)

    def on_joystick_down(self, now:int):
        self.current_screen.on_joystick_down(now)

    def on_start(self, now:int):
        self.current_screen.on_start(now)

    def on_select(self, now:int):
        self.current_screen.on_select(now)

    def on_b(self, now:int):
        handled = self.current_screen.on_b(now)

        if not handled and now - self.last_b_time > 0.5:
            self.cycle_screens()
            self.last_b_time = now