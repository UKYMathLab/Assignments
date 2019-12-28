"""Many aspects of this are taken from the tutorial found here
https://pythonprogramming.net/tkinter-depth-tutorial-making-actual-program/"""

import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk
import itertools as it
from collections import Counter, defaultdict

import numpy as np
import pandas as pd

# https://matplotlib.org/3.1.1/gallery/user_interfaces/embedding_in_tk_sgskip.html
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.animation as animation
from matplotlib import style
style.use("ggplot")

sys.path.append((Path().cwd().parent/"src").as_posix())
from utils.configs import PreprocessingConfig
from preprocessing import preprocess

# f = Figure(figsize=(5,4), dpi=100)
# a = f.add_subplot(111)


def animate(i):
    with open("SampleData.txt", "r") as f:
        data_array = f.read().split("\n")
        xs = []
        ys = []
    for line in data_array:
        if len(line) > 1:
            x, y = line.split(",")
            xs.append(int(x))
            ys.append(int(y))
    a.clear()
    a.plot(xs, ys)


class MasterApplication(tk.Tk):

    def __init__(self, students: list, lab_groups: list, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # change the window icon (requires .ico file) and title
        # tk.Tk.iconbitmap(self, default="ukylogo.ico")
        tk.Tk.wm_title(self, "Math Lab Group Finder")

        # set the base frame
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # store the student and lab group data for other frames
        self.students = students
        self.lab_groups = lab_groups

        # load all frames and display starting frame
        self.frames = {}
        for F in [StartPage, StudentStatsPage, LabGroupStatsPage, ResultsPage]:
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)


    def show_frame(self, controller):
        """Shows the given frame by moving it to the front of the stack."""

        frame = self.frames[controller]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="This is the start page", font=("Verdana",12))
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Student Statistics",
                           command=lambda: controller.show_frame(StudentStatsPage))
        button1.pack(pady=10, padx=10)

        button2 = ttk.Button(self, text="Lab Group Statistics",
                           command=lambda: controller.show_frame(LabGroupStatsPage))
        button2.pack(pady=10, padx=10)

        button3 = ttk.Button(self, text="Results",
                           command=lambda: controller.show_frame(ResultsPage))
        button3.pack(pady=10, padx=10)


class StudentStatsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # label = tk.Label(self, text="This is the start page", font=("Verdana",12))
        # label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                           command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=10, padx=10)

        self.students = controller.students
        self.plot_times()

    def plot_times(self):
        """Plots the frequency of times and preferences for lab groups of students."""
        ALL_TIMES = ["M 8-9", "M 830-930", "M 9-10", "M 930-1030", "M 10-11",
                     "M 1030-1130", "M 11-12", "M 1130-1230", "M 12-1", "M 1230-130",
                     "M 1-2", "M 130-230", "M 2-3", "M 230-330", "M 3-4",
                     "M 330-430", "M 4-5",
                     "T 8-9", "T 830-930", "T 9-10", "T 930-1030", "T 10-11",
                     "T 1030-1130", "T 11-12", "T 1130-1230", "T 12-1", "T 1230-130",
                     "T 1-2", "T 130-230", "T 2-3", "T 230-330", "T 3-4",
                     "T 330-430", "T 4-5",
                     "W 8-9", "W 830-930", "W 9-10", "W 930-1030", "W 10-11",
                     "W 1030-1130", "W 11-12", "W 1130-1230", "W 12-1", "W 1230-130",
                     "W 1-2", "W 130-230", "W 2-3", "W 230-330", "W 3-4",
                     "W 330-430", "W 4-5",
                     "R 8-9", "R 830-930", "R 9-10", "R 930-1030", "R 10-11",
                     "R 1030-1130", "R 11-12", "R 1130-1230", "R 12-1", "R 1230-130",
                     "R 1-2", "R 130-230", "R 2-3", "R 230-330", "R 3-4",
                     "R 330-430", "R 4-5",
                     "F 8-9", "F 830-930", "F 9-10", "F 930-1030", "F 10-11",
                     "F 1030-1130", "F 11-12", "F 1130-1230", "F 12-1", "F 1230-130",
                     "F 1-2", "F 130-230", "F 2-3", "F 230-330", "F 3-4",
                     "F 330-430", "F 4-5"]

        fig = plt.Figure(figsize=(15,8), dpi=100)
        ax = fig.add_subplot(111)

        # initialize counts
        all_time_counts = defaultdict(int, {time:0 for time in ALL_TIMES})

        # count the frequency of times and add to existing counter (defaultdict)
        times = [list(student.available_times) for student in self.students]
        # https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists
        times = list(it.chain.from_iterable(times))
        time_counts = Counter(times)
        for time, count in time_counts.items():
            all_time_counts[time] += count

        all_times = [time for time in all_time_counts.keys()]
        all_counts = [count for count in all_time_counts.values()]
        xs = np.arange(len(ALL_TIMES))
        ys = np.arange(max(all_counts)+1)

        # plot parameters
        ax.bar(xs, all_counts, align="center")
        ax.set_title("Student Availability")
        ax.set_xlabel("Available Times")
        ax.set_ylabel("Number of Students")
        ax.set_xticks(xs)
        ax.set_xticklabels(ALL_TIMES)
        ax.set_yticks(ys)
        ax.xaxis.set_tick_params(rotation=90)

        fig.tight_layout()  # not sure where to put this
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class LabGroupStatsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="This is the start page", font=("Verdana",12))
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                           command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=10, padx=10)


class ResultsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="This is the start page", font=("Verdana",12))
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                           command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=10, padx=10)


if __name__ == "__main__":

    config = PreprocessingConfig()
    student_data, lab_group_data = preprocess(config)

    app = MasterApplication(students=student_data, lab_groups=lab_group_data)

    # ani = animation.FuncAnimation(f, animate, interval=1000)

    app.mainloop()