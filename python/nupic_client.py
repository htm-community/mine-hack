import socket
import random
import numpy as np

from nupic.frameworks.opf.modelfactory import ModelFactory
from nupic.algorithms import anomaly_likelihood

from plotter import MinecraftAnomalyPlotter
from model_params import model_params

HOST = "localhost"
PORT = 50007
# Used for partial socket messages.
socket_buffer = None
anomalyLikelihoodHelper = anomaly_likelihood.AnomalyLikelihood(
  claLearningPeriod=100,
  estimationSamples=100
)

def calculate_radius(point1, point2):
  # print "Calculating distance between points:"
  # print point1
  # print point2
  if point1 is None:
    return 10
  p1 = np.array(point1["location"])
  p2 = np.array(point2["location"])
  dist = np.linalg.norm(p1 - p2)
  time_delta = point2["time"] - point1["time"]
  # print "dist: %f" % dist
  # print "time delta: %i" % time_delta
  blocks_per_second = (dist / time_delta) * 1000
  # print "blocks per second: %f" % blocks_per_second
  return int(round(blocks_per_second))


def process_socket_message(msg):
  global socket_buffer
  lines = msg.split("\n")
  if socket_buffer:
    lines[0] = socket_buffer + lines[0]
  if len(lines[-1]) > 0:
    # Partial message must be buffered
    socket_buffer = lines[-1]
  else:
    socket_buffer = None
  return lines[0:-1]


def socket_cycle(model):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((HOST, PORT))
  print "Waiting for a socket connection..."
  s.listen(1)

  conn, addr = s.accept()

  print "Connected by", addr
  last_point = None
  plotter = MinecraftAnomalyPlotter("Minecraft Location Anomalies")

  while True:
    data = conn.recv(1024)
    if not data: break
    # print "received raw data: " + data
    messages = process_socket_message(data)
    for row in messages:
      # print "\"%s\"" % row
      location, time = tuple(row.split(" "))
      time = int(time)
      xyz = [float(n) for n in location.split(",")]
      vector = np.array(xyz).astype(int)
      this_point = dict(time=time, location=xyz)
      radius = calculate_radius(last_point, this_point)
      last_point = this_point
      modelInput = {
        "vector": (vector, radius)
      }
      result = model.run(modelInput)
      anomalyScore = result.inferences["anomalyScore"]
      anomalyLikelihood = anomalyLikelihoodHelper.anomalyProbability(
        random.random(), anomalyScore
      )
      printHashes(anomalyScore, vector, radius)
      plotter.add(time, xyz[0], xyz[1], xyz[2], radius, anomalyScore, anomalyLikelihood)

  conn.close()


def printHashes(perc, coords, radius, width=50):
  hashes = int(perc * width)
  hashes = ("#" * hashes).ljust(width)
  print "%s x:%i y:%i z:%i %i blocks/s" % (
    hashes, 
    int(coords[0]), 
    int(coords[1]), 
    int(coords[2]), 
    radius
  )


def run():
  params = model_params.MODEL_PARAMS
  model = ModelFactory.create(params)
  model.enableInference({"predictedField": "vector"})
  socket_cycle(model)


if __name__ == "__main__":
  run()

