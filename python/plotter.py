from collections import deque

import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


WINDOW = 300


class MinecraftAnomalyPlotter(object):


  def __init__(self, name):
    self.name = name
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
    self.y = [y]
    self.z = [z]
    self.speed = [speed]
    
    # Setting up charting layouts.
    fig = plt.figure(figsize=(16, 10))
    gs = gridspec.GridSpec(2, 1, height_ratios=[3,  1])

    self._locationGraph = fig.add_subplot(gs[0, 0])
    plt.title("In-Game Location")
    # plt.ylabel('KW Energy Consumption')
    # plt.xlabel('Date')

    self._anomalyGraph = fig.add_subplot(gs[1])

    plt.ylabel('Anomaly Score')
    plt.xlabel('Timestamp')

    # Maximizes window
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())

    plt.tight_layout()

    self.initialized = True


  def add(self, timestamp, x, y, z, speed, anomalyScore):
    if not self.initialized:
      return self._initialize(timestamp, x, y, z, speed, anomalyScore)
    


  def close(self):
    pass