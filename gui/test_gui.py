"""Many aspects of this are taken from the tutorial found here
https://pythonprogramming.net/tkinter-depth-tutorial-making-actual-program/"""

import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk

import numpy as np
import pandas as pd

# https://matplotlib.org/3.1.1/gallery/user_interfaces/embedding_in_tk_sgskip.html
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
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
        label = tk.Label(self, text="This is the start page", font=("Verdana",12))
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                           command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=10, padx=10)

        self.students = controller.students
        f = self.plot_times()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def plot_times(self):
        """Plots the frequency of times and preferences for lab groups of students."""

        fig, axs = plt.subplots(1, 2, sharey=False, tight_layout=True)

        times = [student.available_times for student in self.students]
        unique_times, time_counts = np.unique(set.union(*times), return_counts=True)
        time_xs = np.arange(time_counts)
        axs[0].bar(time_xs, time_counts, align="center")
        axs[0].xticks(time_xs, unique_times)

        # lab_groups = [student.preferences for student in self.students]
        # unique_lab_groups = np.unique([].extend(lab_groups))
        #
        # axs[1].bar(time_xs, time_counts, align="center")
        # axs[1].xticks(time_xs, unique_times)

        return fig


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
