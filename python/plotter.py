from collections import deque

import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.gridspec as gridspec


WINDOW = 300
HIGHLIGHT_ALPHA = 0.3
ANOMALY_HIGHLIGHT_COLOR = 'red'
WEEKEND_HIGHLIGHT_COLOR = 'yellow'
ANOMALY_THRESHOLD = 0.85


def extract_anomaly_indices(likelihoods):
  anomalies_out = []
  anomaly_start = None
  for i, likelihood in enumerate(likelihoods):
    if likelihood >= ANOMALY_THRESHOLD:
      if anomaly_start is None:
        # Mark start of anomaly
        anomaly_start = i
    else:
      if anomaly_start is not None:
        # Mark end of anomaly
        anomalies_out.append((
          anomaly_start, i, ANOMALY_HIGHLIGHT_COLOR, HIGHLIGHT_ALPHA
        ))
        anomaly_start = None

  # Cap it off if we're still in the middle of an anomaly
  if anomaly_start is not None:
    anomalies_out.append((
      anomaly_start, len(likelihoods)-1,
      ANOMALY_HIGHLIGHT_COLOR, HIGHLIGHT_ALPHA
    ))

  return anomalies_out



class MinecraftAnomalyPlotter(object):


  def __init__(self, name):
    self.name = name
    matplotlib.rcParams['legend.fontsize'] = 10
    self.initialized = False
    # For anomaly chart highlights
    self._chartHighlights = []


  def _initialize(self,
                  timestamp,
                  x, y, z,
                  speed,
                  anomaly_score,
                  anomaly_likelihood):
    # Interactive plot for live-updating.
    plt.ion()

    # Local lists of the data to be plotted.
    # The anomaly chart is a rolling window, so populate deques.
    self.timestamps = deque([timestamp] * WINDOW, maxlen=WINDOW)
    self.anomaly_scores = deque([0.0] * WINDOW, maxlen=WINDOW)
    self.anomaly_likelihoods = deque([0.0] * WINDOW, maxlen=WINDOW)
    # The position chart is not rolling, so they can accumulate.
    self.x = [x]
    self.y = [z]
    self.z = [y]
    self.speed = [speed]
    self.timestamps.append(timestamp)
    self.anomaly_scores.append(anomaly_score)
    self.anomaly_likelihoods.append(anomaly_likelihood)

    fig = plt.figure(figsize=(12, 10))
    fig.suptitle("Minecraft Location Anomalies")
    gs = gridspec.GridSpec(2, 1, height_ratios=[3,  1])

    # 3D XYZ plot
    self.plot_3d = plot_3d = fig.add_subplot(gs[0, 0], projection='3d')
    self.location_line = plot_3d.plot3D(self.x, self.y, zs=self.z)[0]

    # Anomaly score line graph
    self.anomaly_plot = plot_anomaly = fig.add_subplot(gs[1])
    plot_anomaly.grid(True)

    anomalyRange = (0.0, 1.0)

    # Plot anomaly score line
    anomaly_score_plot, = plot_anomaly.plot(
      self.timestamps, self.anomaly_scores, 'm'
    )
    anomaly_score_plot.axes.set_ylim(anomalyRange)
    self.anomaly_score_line = anomaly_score_plot

    # Plot anomaly likelihood line
    anomaly_likelihood_plot, = plot_anomaly.plot(
      self.timestamps, self.anomaly_likelihoods, 'r'
    )
    anomaly_likelihood_plot.axes.set_ylim(anomalyRange)
    self.anomaly_likelihood_line = anomaly_likelihood_plot

    plot_anomaly.legend(
      tuple(['anomaly score', 'anomaly likelihood']), loc=3
    )

    plt.tight_layout()
    plt.draw()
    self.initialized = True


  def add(self, timestamp, x, y, z, speed, anomaly_score, anomaly_likelihood):

    if not self.initialized:
      return self._initialize(
        timestamp, x, y, z, speed, anomaly_score, anomaly_likelihood
      )

    # Update data.
    self.x.append(x)
    self.y.append(z)
    self.z.append(y)
    self.timestamps.append(timestamp)
    self.anomaly_scores.append(anomaly_score)
    self.anomaly_likelihoods.append(anomaly_likelihood)
    self.location_line.set_xdata(self.x)
    self.location_line.set_ydata(self.y)
    self.location_line.set_3d_properties(zs=self.z)

    self.plot_3d.set_xlim3d(min(self.x), max(self.x))
    self.plot_3d.set_ylim3d(min(self.y), max(self.y))
    self.plot_3d.set_zlim3d(min(self.z), max(self.z))
    self.plot_3d.autoscale_view(True, True, True)

    self.anomaly_score_line.set_xdata(self.timestamps)
    self.anomaly_score_line.set_ydata(self.anomaly_scores)
    self.anomaly_likelihood_line.set_xdata(self.timestamps)
    self.anomaly_likelihood_line.set_ydata(self.anomaly_likelihoods)

    # Remove previous highlighted regions
    for poly in self._chartHighlights:
      poly.remove()
    self._chartHighlights = []

    anomalies = extract_anomaly_indices(self.anomaly_likelihoods)

    # Highlight anomalies in anomaly chart
    self.highlight_chart(anomalies, self.anomaly_plot)

    self.anomaly_plot.relim()
    self.anomaly_plot.autoscale_view(True, True, True)

    plt.draw()


  def highlight_chart(self, highlights, chart):
    for highlight in highlights:
      # Each highlight contains [start-index, stop-index, color, alpha]
      self._chartHighlights.append(chart.axvspan(
        self.timestamps[highlight[0]], self.timestamps[highlight[1]],
        color=highlight[2], alpha=highlight[3]
      ))


  def close(self):
    plt.ioff()
    plt.show()
