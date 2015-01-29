import os
import socket
import numpy

from plotly import plotly as py
from plotly.tools import set_credentials_file
from plotly.graph_objs import Stream, Data, Scatter, Layout, Figure

from nupic.frameworks.opf.modelfactory import ModelFactory
from model_params import model_params
# from nupic.algorithms import anomaly_likelihood


HOST = 'localhost'
PORT = 50007
PLOTLY_USER = os.environ["PLOTLY_USER"]
PLOTLY_API_KEY = os.environ["PLOTLY_API_KEY"]
PLOTLY_STREAM_ID = os.environ["PLOTLY_STREAM_ID"]

# anomalyLikelihoodHelper = anomaly_likelihood.AnomalyLikelihood()

def socketCycle(model, plot_stream):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((HOST, PORT))
  s.listen(1)

  conn, addr = s.accept()
  plot_stream.open()

  print 'Connected by', addr
  data_count = 0

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
    anomalyScore = result.inferences["anomalyScore"]
    print anomalyScore
    data_count += 1
    data = dict(x=data_count, y=anomalyScore)
    print "Writing to plot.ly:"
    print data
    plot_stream.write(data)

  conn.close()
  plot_stream.close()


def run():
  set_credentials_file(
    username=PLOTLY_USER, 
    api_key=PLOTLY_API_KEY, 
    stream_ids=[PLOTLY_STREAM_ID]
  )
  params = model_params.MODEL_PARAMS
  model = ModelFactory.create(params)
  model.enableInference({"predictedField": "vector"})

  stream_id = Stream(
    token=PLOTLY_STREAM_ID,
    maxpoints=50
  )
  plot = Scatter(
    x=[],
    y=[],
    stream = stream_id,
    name="Minecraft / NuPIC",
  )
  data = Data([plot])
  layout = Layout(title="Minecraft Location Anomalies")
  figure = Figure(data=data, layout=layout)
  plot_stream = py.Stream(PLOTLY_STREAM_ID)
  print py.plot(figure, filename="minecraft-temp")
  
  socketCycle(model, plot_stream)


if __name__ == "__main__":
  run()

