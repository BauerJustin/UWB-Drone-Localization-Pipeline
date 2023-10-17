import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Visualizer:
    def __init__(self, tracker):
        self.tracker = tracker
        self.root = tk.Tk()
        self.root.title("Drone Localization")

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.scatter = self.ax.scatter([], [], [])
        
        self.canvas = self._get_tkinter_canvas()
        self.canvas.get_tk_widget().pack()

        self.root.after(100, self._update)

    def start(self):
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.mainloop()

    def stop(self):
        self._on_close()

    def _on_close(self):
        self.root.destroy()

    def _get_tkinter_canvas(self):
        figure_canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        return figure_canvas

    def _update(self):
        self.ax.clear()
        self.ax.set_xlabel('X axis [m]')
        self.ax.set_ylabel('Y axis [m]')
        self.ax.set_zlabel('Z axis [m]')
        for id in self.tracker.anchor_network.get_anchor_ids():
            x, y, z = self.tracker.anchor_network.get_anchor_position(id)
            self.scatter = self.ax.scatter(x, y, z, c='b', marker='s')
            self.ax.text(x, y, z, id, color='black')
            self._set_min_max_boundaries(x, y, z)

        for id, drone in self.tracker.drones.items():
            x, y, z = drone.get_pos()
            self.scatter = self.ax.scatter(x, y, z, c='r', marker='o')
            self.ax.text(x, y, z, id, color='black')
            self._set_min_max_boundaries(x, y, z)

        self.ax.set_xlim(self.x_min, self.x_max)
        self.ax.set_ylim(self.y_min, self.y_max)
        self.ax.set_zlim(self.z_min, self.z_max)

        self.fig.canvas.draw()
        self.root.after(100, self._update)

    def _set_min_max_boundaries(self, x, y, z):
        self.x_min = min(self.x_min if hasattr(self, 'x_min') else 0, x)
        self.x_max = max(self.x_max if hasattr(self, 'x_max') else 0, x)
        self.y_min = min(self.y_min if hasattr(self, 'y_min') else 0, y)
        self.y_max = max(self.y_max if hasattr(self, 'y_max') else 0, y)
        self.z_min = min(self.z_min if hasattr(self, 'z_min') else 0, z)
        self.z_max = max(self.z_max if hasattr(self, 'z_max') else 0, z)
        