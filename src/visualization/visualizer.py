import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src import constants as const


class Visualizer:
    def __init__(self, tracker):
        self.tracker = tracker
        self.root = tk.Tk()
        self.root.title("Drone Localization")
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.scatter = self.ax.scatter([], [], [])
                
        self.label_frame = tk.Frame(self.root)
        self.label_frame.pack(side=tk.RIGHT, anchor=tk.NE)
        self.drone_labels = {}

        self.dropped_label = tk.Label(self.label_frame)
        self.dropped_label.pack(side=tk.TOP, anchor=tk.NE)
        
        self.canvas = self._get_tkinter_canvas()
        self.canvas.get_tk_widget().pack()

    def start(self):
        print("[Visualizer] Started")
        try:
            self.root.after(100, self._update)
            self.root.mainloop()
        except Exception as e:
            print(f"[Visualizer] Exception occurred: {e}")
            self._on_close()

    def stop(self):
        self._on_close()
        print("[Visualizer] Terminated by user")

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
            pos = self.tracker.anchor_network.get_anchor_pos(id)
            x, y, z = pos.unpack()
            self.scatter = self.ax.scatter(x, y, z, c='b', marker='s')
            self.ax.text(x, y, z, f"{id} ({x:.1f}, {y:.1f}, {z:.1f})", color='black')
            self._set_min_max_boundaries(x, y, z)

        for id, drone in self.tracker.drones.items():
            if drone.active:
                pos = drone.get_pos()
                x, y, z = pos.unpack()
                self.scatter = self.ax.scatter(x, y, z, c='r', marker='o')
                self.ax.text(x, y, z, f"{id} ({x:.2f}, {y:.2f}, {z:.2f})", color='black')

                if drone.has_ground_truth:
                    error = drone.get_euclid_dist()
                    if error >= 0.05:  # only show if error is above 5 cm
                        self.ax.text(x, y, z-0.6, f"Error:{error:.2f}", color='black')
                        if const.PLOT_GROUND_TRUTH:
                            gt = drone.get_ground_truth()
                            gt_x, gt_y, gt_z = gt.unpack()
                            self.scatter = self.ax.scatter(gt_x, gt_y, gt_z, c='g', marker='o')
                            self.ax.text(gt_x, gt_y, gt_z, f'{id}_gt', color='black')

                if id not in self.drone_labels:
                    label = tk.Label(self.label_frame)
                    label.pack(side=tk.TOP, anchor=tk.NE)
                    self.drone_labels[id] = label
                self.drone_labels[id].configure(text=f"Freq {id}: {drone.get_update_frequency():.2f} Hz")

        self.dropped_label.configure(text=f"Dropped packets: {self.tracker.dropped_count}")

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
        