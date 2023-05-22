"""Benchmarking software for human sensory input latency"""

import random
import time
import tkinter as tk
import winsound
from threading import Thread
import pandas as pd

import keyboard


class Logger:
    """A class to log messages"""
    logging_level = 1
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3

    def __init__(self, logging_level=1):
        self.logging_level = logging_level

    def log(self, message, logging_level):
        """A function to log messages"""
        if logging_level >= self.logging_level:
            if logging_level == self.DEBUG:
                print("[DEBUG] " + message)
            elif logging_level == self.INFO:
                print("[INFO] " + message)
            elif logging_level == self.WARNING:
                print("[WARNING] " + message)
            elif logging_level == self.ERROR:
                print("[ERROR] " + message)


l = Logger(logging_level=Logger.INFO)


class Register:
    """A class to log data and store them in an excel file"""
    name = ""
    frame: pd.DataFrame
    temp_time = 0

    def __init__(self, name):
        self.name = name
        self.frame = pd.DataFrame(columns=["Type", "Variation", "Duration", "Reactiontime"])

    def log(self, stimulus, variation, duration):
        """A function to log data and save it in a temporary pandas dataframe"""
        data = pd.Series({"Type": stimulus, "Variation": variation,
                         "Duration": duration, "Reactiontime": self.temp_time})
        self.frame = pd.concat([self.frame, data.to_frame().T], ignore_index=True)

    def save(self):
        """A function to save the data in an excel file"""
        self.frame.to_excel("data/" + self.name + ".xlsx", index=True, header=True)


class Display:
    """A class to display the stimulus using tkinter"""
    root = 0

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sensory Organ tester")
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda e: e.widget.quit())
        self.root.configure(bg="black")

    def update(self):
        """A function to update the display"""
        self.root.update()

    def stimulus(self, duration, color):  # Color must be hex
        """A function to show the stimulus"""
        self.root.configure(bg=color)
        self.root.update()
        self.root.after(duration, self.root.configure(bg="black"))
        self.root.update()


class SensoryOrganTester:
    """A class to test the latency of sensory organs"""
    display = 0
    run = True
    no_of_stimuli = 0

    register = 0

    def __init__(self, no_of_stimuli=10):
        self.no_of_stimuli = no_of_stimuli

    def auditory_stimulus(self):
        """A function to generate an auditory stimulus"""
        frequency = random.randint(50, 7000)
        duration = random.randint(40, 400)
        l.log(
            f"Creating auditory stimulus at frequency {frequency}, duration {duration}", Logger.INFO)
        winsound.Beep(frequency, duration)
        return frequency, duration

    def visual_stimulus(self):
        """A function to generate a visual stimulus"""
        color = random.randint(0, 0xffffff)
        duration = random.randint(10, 400)
        l.log(f"Creating visual stimulus with color {color} and duration {duration}", Logger.INFO)
        self.display.stimulus(duration, f"#{color:06x}")
        return color, duration

    def timer(self):
        """A function to measure the time between the stimulus and the input"""
        time_start = time.time()
        l.log("Timer started", Logger.DEBUG)
        while True:
            if keyboard.is_pressed("space"):
                time_end = time.time()
                l.log("Timer stopped", Logger.DEBUG)
                l.log("Time between stimulus and input: " + str(time_end - time_start), Logger.INFO)
                self.register.temp_time = time_end - time_start
                break

    def startup(self):
        """A function to start the tester"""
        # First, ask for the name of the person
        name = input("Subject Name or Number (first_last):")
        self.register = Register(name)
        l.log(f"Subject {name} registered", Logger.INFO)

        print("Subject registered, test will start in 10 seconds")
        time.sleep(5)
        self.display = Display()
        self.display.update()
        time.sleep(5)
        l.log("Starting benchmark", Logger.INFO)

    def start(self):
        """A function to run the tester"""
        self.startup()

        count = 0
        while self.run:
            count += 1
            if keyboard.is_pressed("escape"):
                l.log("Stopping benchmark", Logger.INFO)
                self.stop()

            if random.randint(0, 1) == 1:  # Visual stimulus
                timer_thread = Thread(target=self.timer)
                timer_thread.start()
                color, duration = self.visual_stimulus()
                timer_thread.join()
                self.register.log("Visual", color, duration)

            else:  # Auditory stimulus
                timer_thread = Thread(target=self.timer)
                timer_thread.start()
                frequency, duration = self.auditory_stimulus()
                timer_thread.join()
                self.register.log("Auditory", frequency, duration)

            time.sleep(random.randint(3, 7))

            if count == self.no_of_stimuli:
                self.register.save()
                l.log("Saved data", Logger.INFO)
                l.log("Stopping benchmark", Logger.INFO)
                self.stop()

    def stop(self):
        """A function to stop the tester"""
        self.run = False
        self.display.root.destroy()


tester = SensoryOrganTester(no_of_stimuli=10)
tester.start()
input("Press enter to exit")
