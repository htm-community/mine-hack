from collections import deque

import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.gridspec as gridspec


WINDOW = 300


class MinecraftAnomalyPlotter(object):


  def __init__(self, name):
    self.name = name
    matplotlib.rcParams['legend.fontsize'] = 10
    self.initialized = False
    

  def _initialize(self, timestamp, x, y, z, speed, anomalyScore):
    # Interactive plot for live-updating.
    plt.ion()

    # Local lists of the data to be plotted.
    # The anomaly chart is a rolling window, so populate deques.
    self.timestamps = deque([timestamp] * WINDOW, maxlen=WINDOW)
    self.anomalyScores = deque([0.0] * WINDOW, maxlen=WINDOW)
    # The position chart is not rolling, so they can accumulate.
    self.x = [x]
    self.y = [z]
    self.z = [y]
    self.speed = [speed]
    
    fig = plt.figure(figsize=(16, 10))
    fig.suptitle("Minecraft Location Anomalies")
    gs = gridspec.GridSpec(2, 1, height_ratios=[3,  1])
    
    # 3D XYZ plot
    self.plot_3d = plot_3d = fig.add_subplot(gs[0, 0], projection='3d')
    self.location_line = plot_3d.plot3D(self.x, self.y, zs=self.z)[0]

    # Anomaly score line graph
    self.anomaly_plot = plot_anomaly = fig.add_subplot(gs[1])
    plot_anomaly.grid(True)
    
    anomalyRange = (0.0, 1.0)
    
    anomalyScorePlot, = plot_anomaly.plot(
      self.timestamps, self.anomalyScores, 'r'
    )
    anomalyScorePlot.axes.set_ylim(anomalyRange)
    
    self.anomalyScoreLine = anomalyScorePlot
    plot_anomaly.legend(
      tuple(['anomaly score']), loc=3
    )

    plt.tight_layout()
    plt.draw()
    self.initialized = True


  def add(self, timestamp, x, y, z, speed, anomalyScore):
    if not self.initialized:
      return self._initialize(timestamp, x, y, z, speed, anomalyScore)
    self.x.append(x)
    self.y.append(z)
    self.z.append(y)
    self.timestamps.append(timestamp)
    self.anomalyScores.append(anomalyScore)
    
    self.location_line.set_xdata(self.x)
    self.location_line.set_ydata(self.y)
    self.location_line.set_3d_properties(zs=self.z)

    self.plot_3d.set_xlim3d(min(self.x), max(self.x))
    self.plot_3d.set_ylim3d(min(self.y), max(self.y))
    self.plot_3d.set_zlim3d(min(self.z), max(self.z))
    self.plot_3d.autoscale_view(True, True, True)
    
    self.anomalyScoreLine.set_xdata(self.timestamps)
    self.anomalyScoreLine.set_ydata(self.anomalyScores)
   
    self.anomaly_plot.relim()
    self.anomaly_plot.autoscale_view(True, True, True)
    
    plt.draw()


  def close(self):
    plt.ioff()
    plt.show()
