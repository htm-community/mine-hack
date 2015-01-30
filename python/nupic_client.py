import socket
import numpy as np

from nupic.frameworks.opf.modelfactory import ModelFactory

from model_params import model_params

HOST = "localhost"                 # Symbolic name meaning the local host
PORT = 50007              # Arbitrary non-privileged port
# Used for partial socket messages.
socket_buffer = None


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


def socket_cycle(model, resultHandler):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((HOST, PORT))
  print "Waiting for a socket connection..."
  s.listen(1)

  conn, addr = s.accept()

  print "Connected by", addr
  last_point = None

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
      resultHandler(result)

  conn.close()


def printHashes(perc, width=50):
  hashes = int(perc * width)
  print "#" * hashes


def predictionResultHandler(result):
  anomalyScore = result.inferences["anomalyScore"]
  printHashes(anomalyScore)


def run():
  params = model_params.MODEL_PARAMS
  model = ModelFactory.create(params)
  model.enableInference({"predictedField": "vector"})
  socket_cycle(model, predictionResultHandler)


if __name__ == "__main__":
  run()

