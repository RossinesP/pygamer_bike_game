from screen import Screen
from tracker import Tracker

from adafruit_display_text import label
import adafruit_imageload
import displayio

import neopixel
import terminalio

MINUTE = 60

class Biker():
    MAX_BIKER_TILES = 4

    def __init__(self, bitmap, palette, primary_color, secondary_color, now:int, x, y):
        self.previous_tick = now
        self.palette = displayio.Palette(len(palette))

        for i in range(len(palette)):
            if i == 1 and primary_color is not None:
                self.palette[i] = primary_color
            elif i == 2 and secondary_color is not None:
                self.palette[i] = secondary_color
            else:
                self.palette[i] = palette[i]

        self.palette.make_transparent(0)

        self.tile_grid = displayio.TileGrid(
            bitmap,
            pixel_shader=self.palette,
            width=1,
            height=1,
            tile_width=16,
            tile_height=22,
            default_tile=0
        )
        self.tile_grid.x = x
        self.tile_grid.y = y

        self.current_tile = 0

    def move(self, x, y):
        self.tile_grid.x = x
        self.tile_grid.y = y

    def update(self, now:int):
        if now - self.previous_tick > 0.2:
            self.current_tile += 1
            self.current_tile %= self.MAX_BIKER_TILES
            self.tile_grid[0] = self.current_tile
            self.previous_tick = now

class Background():
    def __init__(self, bitmap, palette):
        self.tile_grid = displayio.TileGrid(
            bitmap,
            pixel_shader=palette,
            width=20,
            height=16,
            tile_width=8,
            tile_height=8,
            default_tile=1
        )
        for i in range(20):
            self.tile_grid[i, 0] = 2
            self.tile_grid[i, 1] = 0
            self.tile_grid[i, 2] = 1
            self.tile_grid[i, 3] = 1
            self.tile_grid[i, 4] = 1
            self.tile_grid[i, 5] = 0
            self.tile_grid[i, 6] = 2
            self.tile_grid[i, 7] = 2
            self.tile_grid[i, 8] = 2
            self.tile_grid[i, 9] = 0
            self.tile_grid[i, 10] = 1
            self.tile_grid[i, 11] = 1
            self.tile_grid[i, 12] = 1
            self.tile_grid[i, 13] = 0
            self.tile_grid[i, 14] = 2
            self.tile_grid[i, 15] = 2

        self.tile_grid[19,2] = 3
        self.tile_grid[19,3] = 3
        self.tile_grid[19,4] = 3

        self.tile_grid[19,10] = 3
        self.tile_grid[19,11] = 3
        self.tile_grid[19,12] = 3


class TimeSelectionScreen(Screen):
    MAX_DURATION = 60 * MINUTE

    def __init__(self, screen_manager, pixels: neopixel.NeoPixel, tracker: Tracker):
        super().__init__(screen_manager, pixels, tracker)
        self.duration = 15 * MINUTE
        self.last_change_ts = 0

        font = terminalio.FONT
        color = 0xFFFFFF

        self.title = label.Label(font, text="Combien de temps ?", color=color, scale=1)
        self.title.x = 10
        self.title.y = 20

        self.group.append(self.title)
        time = self.get_time_text(self.duration)
        self.time_label = label.Label(font, text=time, color=color, scale= 3)
        self.time_label.x = 25
        self.time_label.y = 60
        self.time_label.anchor_point = (1,0)

        self.group.append(self.time_label)

        self.press_a = label.Label(font, text="Start pour commencer", color=color, scale=1)
        self.press_a.x = 20
        self.press_a.y = 100

        self.group.append(self.press_a)


    def get_time_text(self, duration: int):
        # Beware, duration can be None before the first tick
        if duration:
            # To avoid the length of the string to exceed the allocated length,
            # we reset the hours after 99h.
            # Champions who'd like to break a record are welcome to improve this
            # part.
            hours = (duration / 3600) % 99
            minutes = (duration / 60) % 60
            return f"{hours:01.0f}h {minutes:02.0f}m"
        else:
            return "--:--"

    def on_joystick_up(self, now:int):
        if now - self.last_change_ts > 0.15 and self.duration + MINUTE <= self.MAX_DURATION:
            self.duration += MINUTE
            self.time_label.text = self.get_time_text(self.duration)
            self.last_change_ts = now

    def on_joystick_down(self, now:int):
        if now - self.last_change_ts > 0.15 and self.duration - MINUTE > 0:
            self.duration -= MINUTE
            self.time_label.text = self.get_time_text(self.duration)
            self.last_change_ts = now

    def on_start(self, now:int):
        self.screen_manager.set_ongoing_screen(now, self.duration)

class OngoingGameScreen(Screen):
    STEP_CHOOSE_LEVEL = 0
    STEP_READY = 1
    STEP_BIKING = 2
    STEP_DONE = 3

    def __init__(self, screen_manager, pixels: neopixel.NeoPixel, tracker: Tracker, now: int, duration: int):
        super().__init__(screen_manager, pixels, tracker)
        self.duration = duration
        self.set_state(self.STEP_CHOOSE_LEVEL, now)
        self.last_action_ts = now

    def set_state(self, next_state:int, now:int):
        if next_state == self.STEP_CHOOSE_LEVEL:
            self.init_choose_level_state(now)
        elif next_state == self.STEP_READY:
            self.init_ready_state(now)
        elif next_state == self.STEP_BIKING:
            self.init_biking_state(now)
        elif next_state == self.STEP_DONE:
            self.init_end_state(now)

        self.current_state = next_state

    def init_choose_level_state(self, now:int):
        self.clear_group()


        font = terminalio.FONT
        color = 0xFFFFFF

        self.title = label.Label(font, text="Choose level", color=color, scale=2)
        self.title.x = 10
        self.title.y = 30

        self.group.append(self.title)

        self.level_label = label.Label(font, text="1", color=color, scale=2)
        self.level_label.x = 70
        self.level_label.y = 70

        self.group.append(self.level_label)

        self.set_level(1)

    def init_ready_state(self, now:int):
        self.clear_group()

        font = terminalio.FONT
        color = 0xFFFFFF

        self.title = label.Label(font, text="Ready ?", color=color, scale=2)
        self.title.x = 40
        self.title.y = 60

        self.group.append(self.title)

    def init_biking_state(self, now:int):
        self.clear_group()

        self.start_time = now
        self.start_tick_count = self.tracker.tick_count

        bckgnd_bitmap, bckgnd_palette = adafruit_imageload.load(
            "/bckgnd_sprite.bmp",
            bitmap=displayio.Bitmap,
            palette=displayio.Palette
        )
        self.background = Background(bckgnd_bitmap, bckgnd_palette)
        self.group.append(self.background.tile_grid)

        biker_bitmap, biker_palette = adafruit_imageload.load(
            "/bike_sprite.bmp",
            bitmap=displayio.Bitmap,
            palette=displayio.Palette
        )

        self.biker_goal = Biker(biker_bitmap, biker_palette, (0, 255, 135), (93, 239, 255), 0, x=0, y=16)
        self.group.append(self.biker_goal.tile_grid)

        self.biker_self = Biker(biker_bitmap, biker_palette, None, None, 0, x=0, y=80)
        self.group.append(self.biker_self.tile_grid)

    def init_end_state(self, now:int, player_won=False):
        self.clear_group()

        font = terminalio.FONT
        color = 0xFFFFFF

        if player_won:
            text = "YOU WIN !"
            x = 30
        else:
            text = "YOU LOST =("
            x = 15
        self.title = label.Label(font, text=text, color=color, scale=2)
        self.title.x = x
        self.title.y = 60

        self.group.append(self.title)

    def update_biking_state(self, now:int):
        new_tick_count = self.tracker.tick_count
        diff_tick = new_tick_count - self.start_tick_count
        diff_time = now - self.start_time

        percentage_time = diff_time / float(self.duration)
        if percentage_time >= 1:
            self.init_end_state(now, False)
            self.current_state = self.STEP_DONE

        percentage_tick_count = diff_tick / float(self.target_tick_count)
        if percentage_tick_count >= 1:
            self.init_end_state(now, True)
            self.current_state = self.STEP_DONE

        goal_x_pos = int(percentage_time * 19*8)
        self.biker_goal.move(goal_x_pos, 16)
        self.biker_goal.update(now)

        self_x_pos = int(percentage_tick_count * 19*8)
        self.biker_self.move(self_x_pos, 80)
        self.biker_self.update(now)

    def on_tracker_update(self, now: int):
        if self.current_state == self.STEP_BIKING:
            self.update_biking_state(now)

    def set_level(self, level:int):
        self.level = level
        self.level_label.text = f"{level}"
        target_speed = level / 9.0 * 25000
        self.target_tick_count = int(target_speed / (3 * 3600) * self.duration) # 15 km/h en m/s

    def on_start(self, now:int):
        if now - self.last_action_ts < 1:
            return
        self.last_action_ts = now

        if self.current_state == self.STEP_READY:
            self.set_state(self.STEP_BIKING, now)
        elif self.current_state == self.STEP_DONE:
            self.set_state(self.STEP_READY, now)
        elif self.current_state == self.STEP_CHOOSE_LEVEL:
            self.set_state(self.STEP_READY, now)

    def on_b(self, now:int):
        if self.current_state in [self.STEP_BIKING]:
            return True

        return False

    def on_joystick_down(self, now:int):
        if now - self.last_action_ts < 0.5:
            return
        self.last_action_ts = now

        if self.current_state == self.STEP_CHOOSE_LEVEL:
            if self.level >= 2:
                level = self.level - 1
                self.set_level(level)

    def on_joystick_up(self, now:int):
        if now - self.last_action_ts < 0.5:
            return
        self.last_action_ts = now

        if self.current_state == self.STEP_CHOOSE_LEVEL:
            if self.level <= 8:
                level = self.level + 1
                self.set_level(level)
