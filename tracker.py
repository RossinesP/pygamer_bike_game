import math
# The calories spent for 1 minute of effort is estimated as follows:
# The formula is (MET x body weight in kg x 3.5) / 200
# where MET (Metabolic Equivalent of Task) is :
# 1   on a stationary bike when at rest
# 4.8 on a stationary bike at a lower speed
# 6.8 on a stationary bike at a medium speed
# 11  on a stationary bike at a higher speed
# Let's pretend a lower speed is between 8 and 15 km/h,
# a medium speed is between 15 and 22 km/h
# and a higher speed is > 22 km/h

MET_LOWEST = 1.0
MET_LOWER = 4.8
MET_MEDIUM = 6.8
MET_HIGHEST = 11

LOWER_SPEED = 8.0
MEDIUM_SPEED = 15.0
HIGHER_SPEED = 22.0
BODY_WEIGHT = 85


class Tracker():
    TICK_SAMPLES_COUNT = 4  # Smooth the speed over the previous 10 tick values
    TICK_COUNT = 80
    BIKE_DST_PER_SPIN = 3.9  # TODO : calculate this, in meters
    PREVIOUS_SPEEDS_COUNT = 80 # How many speed values we want to keep. Set to the screen X size / 2

    def __init__(self):
        self.tick_count = 0
        self.previous_ticks = []
        self.max_speed = 0
        self.speed = 0.0
        self.calories = 0.0
        self.start_time = None


    def get_distance(self) -> float:
        return self.BIKE_DST_PER_SPIN * self.tick_count

    def get_speed(self, count_ticks: int, diff_ticks: int) -> float:
        '''
        Returns the speed based on the number of ticks and
        the time between the first and last tick
        '''
        return count_ticks * self.BIKE_DST_PER_SPIN * 3.6 / diff_ticks

    def get_avg_speed(self, now: int) -> tuple:
        tick_length = len(self.previous_ticks)

        if tick_length <= 1:
            return 0.0

        first_tick_index = 0
        samples_index = tick_length - 1 - self.TICK_SAMPLES_COUNT
        if samples_index > first_tick_index:
            first_tick_index = samples_index

        first_tick = self.previous_ticks[first_tick_index]

        tick_count = tick_length - samples_index

        diff_ticks = now - first_tick

        if diff_ticks == 0:
            return 0.0

        speed = self.get_speed(tick_count, diff_ticks)

        if tick_length > 1:
            prev_tick = self.previous_ticks[tick_length - 1]
            diff_ticks = prev_tick - first_tick
            prev_speed = self.get_speed(tick_count, diff_ticks)
            if speed / prev_speed < 0.5:
                speed = 0

        return speed

    def get_calories(self, duration_seconds:int, speed:float):
        if speed < LOWER_SPEED:
            met = MET_LOWEST
        elif speed < MEDIUM_SPEED:
            met = MET_LOWER
        elif speed < HIGHER_SPEED:
            met = MET_MEDIUM
        else:
            met = MET_HIGHEST

        return (met * BODY_WEIGHT * 3.5 * duration_seconds) / (200.0 * 60.0)

    def get_duration(self, now):
        if self.start_time:
            return now - self.start_time
        else:
            return None

    def on_tick(self, timestamp: int):
        if self.tick_count == 0:
            self.start_time = timestamp

        if len(self.previous_ticks) >= self.TICK_COUNT:
            self.previous_ticks = self.previous_ticks[1:]

        self.previous_ticks.append(timestamp)
        self.tick_count += 1

        self.speed = self.get_avg_speed(timestamp)

        previous_ticks_length = len(self.previous_ticks)

        if previous_ticks_length > 1:
            duration_seconds = self.previous_ticks[previous_ticks_length - 1] - self.previous_ticks[previous_ticks_length - 2]
            self.calories += self.get_calories(duration_seconds, self.speed)

        if self.speed > self.max_speed:
            self.max_speed = self.speed

        return self.speed