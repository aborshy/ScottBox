from machine import *
import time


class UpdateException(Exception):
    def __init__(self):
        default_message = 'Tried to update a non-running timer'
        super().__init__(default_message)


# noinspection PyMissingConstructor
class Timer(Pin):

    def __init__(self, led_pin: int, button_pin: int):
        """
        Container that helps organize and manage time-button-clock objects and vars\n
        :rtype: object
        """
        self.led = Pin(led_pin, Pin.OUT)
        self.button = Pin(button_pin, Pin.IN, Pin.PULL_DOWN)
        self.is_running = 0
        self.has_ran = 0
        self.start_time = 0
        self.time = 0
        self.last_value = 0
        self.color = ''  # It crashes when I try putting this as an arg. Whatever. Just assign it after obj creation.
        self.displayed_time = -1

    def check_running(self):
        """
        Returns string saying if timer is running or not. \n
        :return: str
        """
        if self.is_running:
            _ = 'is on'
        else:
            _ = 'is off'
        return _

    def switch_running(self, new_time):
        """
        Switches running state, and updates start_time var to keep current time between pauses
        :param new_time:
        :return: None
        """
        self.is_running = not self.is_running
        self.start_time = new_time - self.time

    def update(self, new_time):
        """
        Updates timer's current time, with time() as an input
        :param new_time:
        :return: None
        """
        if self.has_ran == 0:
            self.start_time = new_time
            self.has_ran = 1
        if self.is_running:
            self.time = (new_time - self.start_time)
        else:
            raise UpdateException


if __name__ == "__main__":
    test = Timer(0, 1)
