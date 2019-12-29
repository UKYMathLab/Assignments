"""Many aspects of this are taken from the tutorial found here
https://pythonprogramming.net/tkinter-depth-tutorial-making-actual-program/"""

import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk
import itertools as it
from collections import Counter

import numpy as np
import pandas as pd

# https://matplotlib.org/3.1.1/gallery/user_interfaces/embedding_in_tk_sgskip.html
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.animation as animation
from matplotlib import style
# style.use("ggplot")

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

        # text
        label = tk.Label(self, text="This is the start page", font=("Verdana",12))

        # buttons
        student_stat_button = ttk.Button(self, text="Student Statistics",
                             command=lambda: controller.show_frame(StudentStatsPage))
        lab_group_stat_button = ttk.Button(self, text="Lab Group Statistics",
                           command=lambda: controller.show_frame(LabGroupStatsPage))
        results_button = ttk.Button(self, text="Results",
                           command=lambda: controller.show_frame(ResultsPage))
        quit_button = ttk.Button(self, text="Quit", command=controller.destroy)

        # page layout
        label.pack(pady=10, padx=10)
        student_stat_button.pack(pady=10, padx=10)
        lab_group_stat_button.pack(pady=10, padx=10)
        results_button.pack(pady=10, padx=10)
        quit_button.pack(pady=10, padx=10)


class StudentStatsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # label = tk.Label(self, text="This is the start page", font=("Verdana",12))
        # label.pack(pady=10, padx=10)

        # buttons
        start_button = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        quit_button = ttk.Button(self, text="Quit", command=controller.destroy)

        # page layout
        start_button.pack(pady=10, padx=10)
        quit_button.pack(pady=10, padx=10)


        self.students = controller.students
        self.plot_times()

    def plot_times(self):
        """Plots the frequency of times and preferences for lab groups of students."""
        ALL_TIMES = ["8-9", "830-930", "9-10", "930-1030", "10-11",
                     "1030-1130", "11-12", "1130-1230", "12-1", "1230-130",
                     "1-2", "130-230", "2-3", "230-330", "3-4",
                     "330-430", "4-5"]
        ALL_DAYS = {"M":"Monday", "T":"Tuesday", "W":"Wednesday", "R":"Thursday", "F":"Friday"}

        formatted_times = [" ".join([day, time]) for day in ALL_DAYS.keys() for time in ALL_TIMES]

        fig = plt.Figure(figsize=(15,8), dpi=100)
        ax = fig.add_subplot(111)

        # initialize counts
        all_time_counts = {time:0 for time in formatted_times}

        # count the frequency of times and add to existing counter (defaultdict)
        times = [list(student.available_times) for student in self.students]
        # https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists
        times = list(it.chain.from_iterable(times))
        time_counts = Counter(times)
        for time, count in time_counts.items():
            all_time_counts[time] += count

        # all_times = [time for time in all_time_counts.keys()]
        all_counts = [count for count in all_time_counts.values()]
        xs = np.arange(len(ALL_TIMES))
        ys = np.arange(len(ALL_DAYS))

        # plot parameters
        # ax.bar(xs, all_counts, align="center")
        ax.set_title("Student Availability")
        ax.set_xlabel("Available Times")
        ax.set_ylabel("Day of the Week")
        ax.set_xticks(xs)
        ax.set_xticklabels(ALL_TIMES)
        ax.set_yticks(ys)
        ax.set_yticklabels(ALL_DAYS.values())
        ax.xaxis.set_tick_params(rotation=90)

        # https://stackoverflow.com/questions/14777066/matplotlib-discrete-colorbar
        cmap = matplotlib.cm.get_cmap("viridis", max(all_counts)+1)
        im = ax.imshow(np.array(all_counts).reshape( (len(ALL_DAYS), len(ALL_TIMES)) ),
                       cmap=cmap, vmin=-0.5, vmax=max(all_counts)+0.5)
        cbar = fig.colorbar(im, ax=ax, ticks=np.arange(max(all_counts)+1))
        cbar.set_label("Number of Students", rotation=270)

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

        # buttons
        start_button = ttk.Button(self, text="Back to Home",
                                  command=lambda: controller.show_frame(StartPage))
        quit_button = ttk.Button(self, text="Quit", command=controller.destroy)

        # page layout
        start_button.pack(pady=10, padx=10)


class ResultsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="This is the start page", font=("Verdana",12))
        label.pack(pady=10, padx=10)

        # buttons
        start_button = ttk.Button(self, text="Back to Home",
                                  command=lambda: controller.show_frame(StartPage))
        quit_button = ttk.Button(self, text="Quit", command=controller.destroy)

        # page layout
        start_button.pack(pady=10, padx=10)


if __name__ == "__main__":

    config = PreprocessingConfig()
    student_data, lab_group_data = preprocess(config)

    app = MasterApplication(students=student_data, lab_groups=lab_group_data)

    # ani = animation.FuncAnimation(f, animate, interval=1000)

    app.mainloop()
