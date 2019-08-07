from __future__ import print_function
import json

from bokeh.embed import json_item,components
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.sampledata.iris import flowers

from flask import Flask,make_response
from jinja2 import Template
from flask_cors import CORS
import pandas as pd


app = Flask(__name__)
CORS(app, resources=r'/*')

page = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
  {{ resources }}
</head>
<body>
  <div id="circle1"></div>
  <div id="circle2"></div>
  <div id="line1"></div>
  <div id="surface1"></div>
  <div id="bar1"></div>
  <script>
  fetch('/circle1')
    .then(function(response) { return response.json(); })
    .then(function(item) { Bokeh.embed.embed_item(item,"circle1"); })
  </script>
  <script>
  fetch('/circle2')
    .then(function(response) { return response.json(); })
    .then(function(item) { Bokeh.embed.embed_item(item, "circle2"); })
  </script>
  <script>
  fetch('/line1')
    .then(function(response) { return response.json(); })
    .then(function(item) { Bokeh.embed.embed_item(item, "line1"); })
  </script>
  <script>
  fetch('/scatter1')
    .then(function(response) { return response.json(); })
    .then(function(item) { Bokeh.embed.embed_item(item, "scatter1"); })
  </script>
  <script>
  fetch('/bar1')
    .then(function(response) { return response.json(); })
    .then(function(item) { Bokeh.embed.embed_item(item, "bar1"); })
  </script>
</body>
""")

page2=Template("""
<!DOCTYPE html>
<html lang="en">
<head>
  {{ resources }}
</head>
<body>
  <div id="scatter1"></div>
  <script>
  fetch('/scatter1')
    .then(function(response) { return response.json(); })
    .then(function(item) { Bokeh.embed.embed_item(item,"scatter1"); })
  </script>
</body>
""")

colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
colors = [colormap[x] for x in flowers['species']]

@app.route('/')
def root():
    return page.render(resources=CDN.render())


@app.route('/singleRender')
def srd():
  response=make_response(page2.render(resources=CDN.render()))
  response.headers['Access-Control-Allow-Origin'] = '*'
  response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
  response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
  
  return response
  # return page2.render(resources=CDN.render())

@app.route('/getimg')
def getimg():
  file=open('1.jpg','rb')
  data=file.read()
  response=make_response(data)
  response.headers['Access-Control-Allow-Origin'] = '*'
  response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
  response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
  return response

@app.route('/img1com')
def img1com():
  from PIL import Image
  import numpy as np
  p = figure(title = "circle1 Iris Morphology", sizing_mode="fixed", plot_width=625, plot_height=400)
  p.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
  p.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks

  p.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
  p.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks
  p.xaxis.major_label_text_font_size = '0pt'  # turn off x-axis tick labels
  p.yaxis.major_label_text_font_size = '0pt'  # turn off y-axis tick labels
  p.image_url(url=["http://140.112.26.135:8787/getimg"], x=0, y=0, w=1200, h=675,anchor='bottom_left')
  script,div=components(p,wrap_script=False)
  response=make_response(json.dumps({"div":div,"script":script}))
  response.headers['Access-Control-Allow-Origin'] = '*'
  response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
  response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
  return response
  # return json.dumps({"div":div,"script":script})

@app.route('/circle1com')
def circle1com():
    p = figure(title = "circle1 Iris Morphology", sizing_mode="fixed", plot_width=625, plot_height=400)
    p.xaxis.axis_label = 'petal_width'
    p.yaxis.axis_label = 'petal_length'
    p.circle(flowers['petal_width'], flowers['petal_length'], color=colors, fill_alpha=0.2, size=10)
    script,div=components(p,wrap_script=False)
    return json.dumps({"div":div,"script":script})

@app.route('/circle1')
def circle1():
    p = figure(title = "circle1 Iris Morphology", sizing_mode="fixed", plot_width=600, plot_height=400)
    p.xaxis.axis_label = 'petal_width'
    p.yaxis.axis_label = 'petal_length'
    p.circle(flowers['petal_width'], flowers['petal_length'], color=colors, fill_alpha=0.2, size=10)
    return json.dumps(json_item(p))

@app.route('/circle2')
def circle2():
    p = figure(title = "circle2 Iris Morphology", sizing_mode="fixed", plot_width=600, plot_height=400)
    p.xaxis.axis_label = 'sepal_width'
    p.yaxis.axis_label = 'sepal_length'
    p.circle(flowers['sepal_width'], flowers['sepal_length'],  fill_alpha=0.2, size=10)
    return json.dumps(json_item(p))

@app.route('/line1')
def line1():
    import pandas as pd
    speed = [4, 4, 7, 7, 8, 9, 10, 10, 10, 11, 11, 12, 12, 12, 12, 13, 13, 13, 13, 14, 14, 14, 14, 15, 15, 15, 16, 16, 17, 17, 17, 18, 18, 18, 18, 19, 19, 19, 20, 20, 20, 20, 20, 22, 23, 24, 24, 24, 24, 25]
    dist = [2, 10, 4, 22, 16, 10, 18, 26, 34, 17, 28, 14, 20, 24, 28, 26, 34, 34, 46, 26, 36, 60, 80, 20, 26, 54, 32, 40, 32, 40, 50, 42, 56, 76, 84, 36, 46, 68, 32, 48, 52, 56, 64, 66, 54, 70, 92, 93, 120, 85]
    p=figure(title = "line1", sizing_mode="fixed", plot_width=600, plot_height=400)
    p.xaxis.axis_label = "SPEED"
    p.yaxis.axis_label = "dist"
    p.line(speed,dist)
    return json.dumps(json_item(p))

@app.route('/scatter1')
def surface1():
  p=figure(title = "scatter1", sizing_mode="fixed", plot_width=600, plot_height=400)
  p.scatter(flowers['sepal_width'],flowers['sepal_length'], color=colors)
  return json.dumps(json_item(p))

@app.route('/bar1')
def bar1():
  flowers=pd.read_csv('1.csv')
  cnt=[[str(x),list(flowers['species']).count(x)] for x in set(flowers['species'])]
  p=figure(x_range=[d[0] for d in cnt],title = "bar1", sizing_mode="fixed", plot_width=600, plot_height=400)
  p.vbar(x=[d[0] for d in cnt], top=[d[1] for d in cnt], width=0.9)
  return json.dumps(json_item(p))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8787)