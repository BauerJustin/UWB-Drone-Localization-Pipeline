import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
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

    def plot_history(self, plot_best_fit=False):
        print("[Visualizer] Plotting all points")
        self.ax.clear()
        self._plot_anchors()
        for history in self.tracker.drones_history.values():
            x_points, y_points, z_points = [], [], []
            for pos in history:
                x, y, z = pos.unpack()
                x_points.append(x)
                y_points.append(y)
                z_points.append(z)
            self.scatter = self.ax.scatter(x_points, y_points, z_points, c=np.linspace(0, 1, len(x_points)), cmap=plt.cm.RdYlGn, marker='.')
            if plot_best_fit:
                X = np.column_stack((x_points, y_points, np.ones(len(x_points))))
                params = np.linalg.lstsq(X, z_points, rcond=None)[0]
                x_fit = np.linspace(min(x_points), max(x_points), 100)
                y_fit = np.linspace(min(y_points), max(y_points), 100)
                x_fit, y_fit = np.meshgrid(x_fit, y_fit)
                z_fit = params[0] * x_fit + params[1] * y_fit + params[2]
                self.ax.plot_surface(x_fit, y_fit, z_fit, alpha=0.5, rstride=100, cstride=100, color='blue')
        self._plot_axes()
        self.fig.canvas.draw()
        try:
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
        self._plot_anchors()
        for id, drone in self.tracker.drones.items():
            if drone.active:
                self._plot_drone_with_metrics(id, drone)
        self._plot_axes()
        self.fig.canvas.draw()
        self.root.after(100, self._update)

    def _plot_anchors(self):
        for id in self.tracker.anchor_network.get_anchor_ids():
            pos = self.tracker.anchor_network.get_anchor_pos(id)
            x, y, z = pos.unpack()
            self.scatter = self.ax.scatter(x, y, z, c='b', marker='s')
            self.ax.text(x, y, z, f"{id} ({x:.1f}, {y:.1f}, {z:.1f})", color='black')
            self._set_min_max_boundaries(x, y, z)

    def _plot_drone_with_metrics(self, id, drone):
        pos = drone.get_pos()
        x, y, z = pos.unpack()
        self.scatter = self.ax.scatter(x, y, z, c='r', marker='o')
        self.ax.text(x, y, z, f"{id} ({x:.2f}, {y:.2f}, {z:.2f})", color='black')
        if drone.has_ground_truth:
            error = drone.get_euclid_dist()
            if error >= const.PLOT_ERROR_MIN:
                self.ax.text(x, y, z-0.6, f"Error:{error:.2f}", color='black')
                if const.PLOT_GROUND_TRUTH:
                    gt = drone.get_ground_truth()
                    gt_x, gt_y, gt_z = gt.unpack()
                    self.scatter = self.ax.scatter(gt_x, gt_y, gt_z, c='g', marker='o')
                    self.ax.text(gt_x, gt_y, gt_z, f'{id}_gt', color='black')

        metrics = {}
        metrics[f'Freq {id}'] = f'{drone.get_update_frequency():.2f} Hz'
        drone_var = drone.get_variance()
        metrics[f'X_var {id}'] = f'{drone_var[0]:.2f} m'
        metrics[f'Y_var {id}'] = f'{drone_var[1]:.2f} m'
        metrics[f'Z_var {id}'] = f'{drone_var[2]:.2f} m'

        for title, metric in metrics.items():
            if title not in self.drone_labels:
                label = tk.Label(self.label_frame)
                label.pack(side=tk.TOP, anchor=tk.NE)
                self.drone_labels[title] = label
            self.drone_labels[title].configure(text=f"{title}: {metric}")

        self.dropped_label.configure(text=f"Dropped measurements: {self.tracker.dropped_measurements}")

    def _plot_axes(self):
        self.ax.set_xlabel('X axis [m]')
        self.ax.set_ylabel('Y axis [m]')
        self.ax.set_zlabel('Z axis [m]')
        self.ax.set_xlim(self.x_min, self.x_max)
        self.ax.set_ylim(self.y_min, self.y_max)
        self.ax.set_zlim(self.z_min, self.z_max)

    def _set_min_max_boundaries(self, x, y, z):
        self.x_min = min(self.x_min if hasattr(self, 'x_min') else 0, x)
        self.x_max = max(self.x_max if hasattr(self, 'x_max') else 0, x)
        self.y_min = min(self.y_min if hasattr(self, 'y_min') else 0, y)
        self.y_max = max(self.y_max if hasattr(self, 'y_max') else 0, y)
        self.z_min = min(self.z_min if hasattr(self, 'z_min') else 0, z)
        self.z_max = max(self.z_max if hasattr(self, 'z_max') else 0, z)
        