import socket
import numpy

from nupic.frameworks.opf.modelfactory import ModelFactory

from model_params import model_params

HOST = 'localhost'                 # Symbolic name meaning the local host
PORT = 50007              # Arbitrary non-privileged port


def socketCycle(model, resultHandler):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((HOST, PORT))
  s.listen(1)

  conn, addr = s.accept()

  print 'Connected by', addr

  while True:
    data = conn.recv(1024)
    if not data: break
    vector = numpy.array(
      [int(float(n)) for n in data.split('\n')[0].split(',')]
    )
    radius = 10
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
  socketCycle(model, predictionResultHandler)


if __name__ == "__main__":
  run()

