"""A programm to test the latency of human input after a given stimulus"""
import winsound
import random
import time
from threading import Thread
import keyboard


def auditory_stimulus():
    """A function to generate an auditory stimulus"""
    frequency = random.randint(100, 1000)
    duration = random.randint(100, 1000)
    print("Beep")
    winsound.Beep(frequency, duration)
    print("Auditory stimulus generated")


def timer():
    """A function to measure the time between the stimulus and the input"""
    time_start = time.time()
    print("Timer started")
    while True:
        if keyboard.is_pressed("space"):
            time_end = time.time()
            print("Timer stopped")
            print("Time between stimulus and input: " + str(time_end - time_start))
            break


if __name__ == "__main__":
    while True:
        timer_thread = Thread(target=timer)
        timer_thread.start()
        auditory_stimulus()
        timer_thread.join()
        time.sleep(5)
