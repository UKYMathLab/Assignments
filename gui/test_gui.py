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
style.use("ggplot")

sys.path.append((Path().cwd().parent/"src").as_posix())
from utils.configs import PreprocessingConfig
from preprocessing import preprocess


# taken from here https://gist.github.com/novel-yet-trivial/3eddfce704db3082e38c84664fc1fdf8
# from this Reddit post https://www.reddit.com/r/learnpython/comments/8ohyvo/tkinter_scrollbar_in_python_36/
class VerticalScrolledFrame:
    """
    A vertically scrolled Frame that can be treated like any other Frame
    ie it needs a master and layout and it can be a master.
    :width:, :height:, :bg: are passed to the underlying Canvas
    :bg: and all other keyword arguments are passed to the inner Frame
    note that a widget layed out in this frame will have a self.master 3 layers deep,
    (outer Frame, Canvas, inner Frame) so
    if you subclass this there is no built in way for the children to access it.
    You need to provide the controller separately.
    """
    def __init__(self, master, **kwargs):
        width = kwargs.pop('width', None)
        height = kwargs.pop('height', None)
        bg = kwargs.pop('bg', kwargs.pop('background', None))
        self.outer = tk.Frame(master, **kwargs)

        self.vsb = tk.Scrollbar(self.outer, orient=tk.VERTICAL)
        self.vsb.pack(fill=tk.Y, side=tk.RIGHT)
        self.canvas = tk.Canvas(self.outer, highlightthickness=0, width=width, height=height, bg=bg)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas['yscrollcommand'] = self.vsb.set
        # mouse scroll does not seem to work with just "bind"; You have
        # to use "bind_all". Therefore to use multiple windows you have
        # to bind_all in the current widget
        self.canvas.bind("<Enter>", self._bind_mouse)
        self.canvas.bind("<Leave>", self._unbind_mouse)
        self.vsb['command'] = self.canvas.yview

        self.inner = tk.Frame(self.canvas, bg=bg)
        # pack the inner Frame into the Canvas with the topleft corner 4 pixels offset
        self.canvas.create_window(4, 4, window=self.inner, anchor='nw')
        self.inner.bind("<Configure>", self._on_frame_configure)

        self.outer_attr = set(dir(tk.Widget))

    def __getattr__(self, item):
        if item in self.outer_attr:
            # geometry attributes etc (eg pack, destroy, tkraise) are passed on to self.outer
            return getattr(self.outer, item)
        else:
            # all other attributes (_w, children, etc) are passed to self.inner
            return getattr(self.inner, item)

    def _on_frame_configure(self, event=None):
        x1, y1, x2, y2 = self.canvas.bbox("all")
        height = self.canvas.winfo_height()
        self.canvas.config(scrollregion = (0,0, x2, max(y2, height)))

    def _bind_mouse(self, event=None):
        self.canvas.bind_all("<4>", self._on_mousewheel)
        self.canvas.bind_all("<5>", self._on_mousewheel)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mouse(self, event=None):
        self.canvas.unbind_all("<4>")
        self.canvas.unbind_all("<5>")
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        """Linux uses event.num; Windows / Mac uses event.delta"""
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units" )
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units" )


class Container(tk.Frame):
    """Frame that holds all of the necessary framework of the rest of the frames."""

    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        # fill the entire frame
        self.pack(side="top", fill="both", expand=True)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.add_menu()


    def add_menu(self):
        """Adds a navigation menu to the frame. Taken from this tutorial:
        https://pythonprogramming.net/tkinter-menu-bar-tutorial/"""

        nav_menu = tk.Menu(self.parent)
        self.parent.config(menu=nav_menu)

        # add file button to menu and add its commands
        file = tk.Menu(nav_menu)
        file.add_command(label="Home",
                         command=lambda: self.parent.show_frame(StartFrame))
        file.add_command(label="Exit", command=self.parent.destroy)


        # do the same for the view button
        view = tk.Menu(nav_menu)
        view.add_command(label="Student Statistics",
                         command=lambda: self.parent.show_frame(StudentStatsFrame))
        view.add_command(label="Lab Group Statistics",
                         command=lambda: self.parent.show_frame(LabGroupStatsFrame))
        view.add_command(label="Results",
                         command=lambda: self.parent.show_frame(ResultsFrame))

        # add the dropdown menus to the nav menu
        nav_menu.add_cascade(label="File", menu=file)
        nav_menu.add_cascade(label="View", menu=view)


class MasterApplication(tk.Tk):
    """Controls the display of all frames."""

    def __init__(self, students: list, lab_groups: list, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # change the window icon (requires .ico file) and title
        # tk.Tk.iconbitmap(self, default="ukylogo.ico")
        tk.Tk.wm_title(self, "Math Lab Group Finder")

        # set the base frame
        container = Container(self)

        # store the student and lab group data for other frames
        self.students = students
        self.lab_groups = lab_groups

        # these might change depending on the Google Form questions
        self.ALL_TIMES = ["8-9", "830-930", "9-10", "930-1030", "10-11",
                          "1030-1130", "11-12", "1130-1230", "12-1", "1230-130",
                          "1-2", "130-230", "2-3", "230-330", "3-4",
                          "330-430", "4-5"]
        self.ALL_DAYS = {"M":"Monday", "T":"Tuesday", "W":"Wednesday", "R":"Thursday", "F":"Friday"}
        self.FORMATTED_TIMES = [" ".join([day, time]) for day in self.ALL_DAYS.keys() for time in self.ALL_TIMES]

        # load all frames and display starting frame
        self.frames = {}
        for F in [StartFrame, StudentStatsFrame, LabGroupStatsFrame, ResultsFrame]:
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartFrame)


    def show_frame(self, controller):
        """Shows the given frame by moving it to the front of the stack."""

        frame = self.frames[controller]
        frame.tkraise()


class StartFrame(tk.Frame):
    """Frame that is displayed at the startup of the GUI. Can navigate to any frame."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        # text
        label = tk.Label(self, text="Welcome!", font=("Verdana",12))

        # frame layout
        label.pack(pady=10, padx=10)


class StudentStatsFrame(VerticalScrolledFrame):
    """Frame for displaying plots to visualize the student data."""

    def __init__(self, parent, controller):
        VerticalScrolledFrame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.students = controller.students
        self.show_plots(controller)


    def plot_time_colored(self, row_num: int=0):
        """Creates a plot that shows the number of students who have a particular
        time on a particualar day available."""

        xs = np.arange(len(self.controller.ALL_TIMES))
        ys = np.arange(len(self.controller.ALL_DAYS))

        # plot parameters
        # ax.bar(xs, all_counts, align="center")
        self.axes[row_num].set_xlabel("Times")
        self.axes[row_num].set_ylabel("Day of the Week")
        self.axes[row_num].set_xticks(xs)
        self.axes[row_num].set_xticklabels(self.controller.ALL_TIMES)
        self.axes[row_num].set_yticks(ys)
        self.axes[row_num].set_yticklabels(self.controller.ALL_DAYS.values())
        self.axes[row_num].xaxis.set_tick_params(rotation=90, labelsize=8)
        self.axes[row_num].yaxis.set_tick_params(labelsize=8)
        self.axes[row_num].grid(None)


        # https://stackoverflow.com/questions/14777066/matplotlib-discrete-colorbar
        cmap = matplotlib.cm.get_cmap("Reds_r", max(self.all_counts)+1)
        im = self.axes[row_num].imshow(np.array(self.all_counts).reshape( (len(self.controller.ALL_DAYS), len(self.controller.ALL_TIMES)) ),
                                       cmap=cmap, vmin=-0.5, vmax=max(self.all_counts)+0.5)
        cbar = self.fig.colorbar(im, ax=self.axes[row_num], ticks=np.arange(max(self.all_counts)+1))
        cbar.set_label("Number of Students", rotation=270)


    def plot_time_hist(self, row_num):
        """Creates a plot that shows the number of students with particular time
        availabilities (shown across ALL possible times)."""

        xs = np.arange(len(self.controller.FORMATTED_TIMES))
        ys = np.arange(len(self.students))

        # plot parameters
        self.axes[row_num].bar(xs, self.all_counts, align="center")
        self.axes[row_num].set_xlabel("Days/Times")
        self.axes[row_num].set_ylabel("Number of Students")
        self.axes[row_num].set_xticks(xs)
        self.axes[row_num].set_xticklabels(self.controller.FORMATTED_TIMES)
        self.axes[row_num].set_yticks(ys)
        self.axes[row_num].xaxis.set_tick_params(rotation=90, labelsize=8)
        self.axes[row_num].yaxis.set_tick_params(labelsize=8)


    def show_plots(self, controller):
        """Plots the frequency of times and preferences for lab groups of students."""

        self.fig, self.axes = plt.subplots(nrows=2, ncols=1, figsize=(12,10), dpi=100)

        # initialize counts
        all_time_counts = {time:0 for time in self.controller.FORMATTED_TIMES}

        # count the frequency of times and add to existing counter (defaultdict)
        times = [list(student.available_times) for student in self.students]
        # https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists
        times = list(it.chain.from_iterable(times))
        time_counts = Counter(times)
        for time, count in time_counts.items():
            all_time_counts[time] += count
        self.all_counts = [count for count in all_time_counts.values()]

        # construct the plots and adjst sizes if necessary
        self.plot_time_colored(0)
        self.plot_time_hist(1)
        self.fig.suptitle("Student Availability", fontsize="xx-large")
        # plt.subplots_adjust(hspace=0.5)

        canvas = FigureCanvasTkAgg(self.fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class LabGroupStatsFrame(tk.Frame):
    """Frame for displaying plots to visualize the lab group data."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        label = tk.Label(self, text="Under construction.", font=("Verdana",12))
        label.pack(pady=10, padx=10)


class ResultsFrame(tk.Frame):
    """Frame for displaying the results from assignment algorithm."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        label = tk.Label(self, text="Under construction.", font=("Verdana",12))
        label.pack(pady=10, padx=10)


if __name__ == "__main__":

    config = PreprocessingConfig()
    student_data, lab_group_data = preprocess(config)

    app = MasterApplication(students=student_data, lab_groups=lab_group_data)
    app.mainloop()
