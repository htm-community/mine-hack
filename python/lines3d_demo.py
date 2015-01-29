import random
import time
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

mpl.rcParams['legend.fontsize'] = 10

plt.ion()

fig = plt.figure()
ax = fig.gca(projection='3d')

x = []
y = []
z = []

for i in xrange(100):
  x.append(random.uniform(0, i))
  y.append(random.uniform(0, i))
  z.append(random.uniform(0, i))

line = [x, y, z]

while True:
  x.append(random.uniform(0, 100))
  y.append(random.uniform(0, 100))
  z.append(random.uniform(0, 100))
  ax.plot(x, y, z)
  plt.draw()
  time.sleep(0.5)

