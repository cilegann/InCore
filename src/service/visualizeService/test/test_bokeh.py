from __future__ import print_function
import json

from bokeh.embed import json_item,components
from bokeh.plotting import figure,show
from bokeh.resources import CDN
from bokeh.sampledata.iris import flowers
from bokeh.models import CustomJS,SaveTool,Tool,CustomAction,HoverTool,CustomJSHover,ColumnDataSource,Range1d,Slider
from bokeh.layouts import column
from flask import Flask,make_response
from jinja2 import Template
from flask_cors import CORS
import pandas as pd
import numpy as np


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
  <div id="scatter1"></div>
  <div id="bar1"></div>
  <div id="his1"></div>
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
  <script>
  fetch('/histogram1')
    .then(function(response) { return response.json(); })
    .then(function(item) { Bokeh.embed.embed_item(item, "his1"); })
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
  <div id="page2"></div>
  <script>
  fetch('/scatterSelect')
    .then(function(response) { return response.json(); })
    .then(function(item) { Bokeh.embed.embed_item(item,"page2"); })
  </script>
</body>
""")


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

@app.route('/downloadimg')
def dlimg():
  file=open('1.jpg','rb')
  data=file.read()
  response=make_response(data)
  response.headers['Access-Control-Allow-Origin'] = '*'
  response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
  response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
  response.headers['Content-Type']='application/octet-stream; charset=utf-8'
  response.headers['Content-Disposition'] = 'attachment; filename=test.png'
  return response


saveCallback=CustomJS(code="""window.open('http://140.112.26.135:8787/"""+"""downloadimg"""+"""');""")


@app.route('/img1com')
def img1com():
  from PIL import Image
  import numpy as np
  # newsave=SaveTool(callback=saveCallback)
  p = figure(title = "circle1 Iris Morphology", sizing_mode="fixed", plot_width=625, plot_height=400,tools='pan,wheel_zoom,box_zoom,reset')
  p.add_tools(CustomAction(icon="save_icon.png",callback=saveCallback))
  p.toolbar.logo=None
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
    
    colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
    colors = [colormap[x] for x in flowers['species']]
    p = figure(title = "circle1 Iris Morphology", sizing_mode="fixed", plot_width=625, plot_height=400,tools='pan,wheel_zoom,box_zoom,save,reset')
    p.toolbar.logo=None
    p.xaxis.axis_label = 'petal_width'
    p.yaxis.axis_label = 'petal_length'
    source=ColumnDataSource(flowers)
    from bokeh.transform import factor_cmap
    p.circle(flowers['petal_width'], flowers['petal_length'],source=source, color=colors, fill_alpha=0.2, size=10)
    script,div=components(p,wrap_script=False)
    return json.dumps({"div":div,"script":script})

@app.route('/circle1')
def circle1():
    
    colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
    colors = [colormap[x] for x in flowers['species']]
    p = figure(title = "circle1 Iris Morphology", sizing_mode="fixed", plot_width=600, plot_height=400,tools='pan,wheel_zoom,box_zoom,reset,save')
    p.toolbar.logo=None
    p.xaxis.axis_label = 'petal_width'
    p.yaxis.axis_label = 'petal_length'
    p.add_tools(
      HoverTool(
        show_arrow=True, 
        line_policy='next',
        tooltips=[
            ('X_value', '$data_x'),
            ('Y_value', '$data_y')
        ]
      )
    )
    p.circle(flowers['petal_width'], flowers['petal_length'], color=colors, fill_alpha=0.2, size=10)
    return json.dumps(json_item(p))

@app.route('/circle2')
def circle2():
    p = figure(title = "circle2 Iris Morphology", sizing_mode="fixed", plot_width=600, plot_height=400,tools='pan,wheel_zoom,box_zoom,save,reset')
    p.toolbar.logo=None
    p.xaxis.axis_label = 'sepal_width'
    p.yaxis.axis_label = 'sepal_length'
    p.add_tools(
      HoverTool(
        show_arrow=True, 
        line_policy='next',
        tooltips=[
            ('X_value', '$data_x'),
            ('Y_value', '$data_y')
        ]
      )
    )
    p.circle(flowers['sepal_width'], flowers['sepal_length'],  fill_alpha=0.2, size=10)
    return json.dumps(json_item(p))

@app.route('/line1')
def line1():
    import pandas as pd
    speed = [4, 4, 7, 7, 8, 9, 10, 10, 10, 11, 11, 12, 12, 12, 12, 13, 13, 13, 13, 14, 14, 14, 14, 15, 15, 15, 16, 16, 17, 17, 17, 18, 18, 18, 18, 19, 19, 19, 20, 20, 20, 20, 20, 22, 23, 24, 24, 24, 24, 25]
    dist = [2, 10, 4, 22, 16, 10, 18, 26, 34, 17, 28, 14, 20, 24, 28, 26, 34, 34, 46, 26, 36, 60, 80, 20, 26, 54, 32, 40, 32, 40, 50, 42, 56, 76, 84, 36, 46, 68, 32, 48, 52, 56, 64, 66, 54, 70, 92, 93, 120, 85]
    p=figure(title = "line1", sizing_mode="fixed", plot_width=600, plot_height=400,tools='pan,wheel_zoom,box_zoom,save,reset')
    p.toolbar.logo=None
    p.xaxis.axis_label = "SPEED"
    p.yaxis.axis_label = "dist"
    p.add_tools(
      HoverTool(
        show_arrow=True, 
        line_policy='next',
        tooltips=[
            ('X_value', '$data_x'),
            ('Y_value', '$data_y')
        ]
      )
    )
    p.line(speed,dist)
    return json.dumps(json_item(p))

@app.route('/scatter1')
def scatter1():
  colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
  colors = [colormap[x] for x in flowers['species']]
  p=figure(title = "scatter1", sizing_mode="fixed", plot_width=600, plot_height=400,tools='pan,wheel_zoom,box_zoom,save,reset')
  p.toolbar.logo=None
  p.add_tools(
    HoverTool(
      show_arrow=True, 
      line_policy='next',
      tooltips=[
          ('X_value', '$data_x'),
          ('Y_value', '$data_y')
      ]
    )
  )
  p.scatter(flowers['sepal_width'],flowers['sepal_length'], color=colors)
  return json.dumps(json_item(p))

@app.route('/bar1')
def bar1():
  flowers=pd.read_csv('1.csv')
  cnt=[[x,list(flowers['species']).count(x)] for x in set(flowers['species'])]
  p=figure(title = "bar1", sizing_mode="fixed", plot_width=600, plot_height=400,tools='pan,wheel_zoom,box_zoom,save,reset')
  p.x_range=Range1d(0,4)#[d[0] for d in cnt]
  p.yaxis.axis_label = "count"
  p.toolbar.logo=None
  source = ColumnDataSource(pd.DataFrame({'counts':[d[1] for d in cnt],'x':[d[0] for d in cnt]}) )
  p.add_tools(
    HoverTool(
      show_arrow=False, 
      line_policy='next',
      tooltips=[
          ('count', '@counts'),
      ]
    )
  )
  p.vbar(source=source,x='x', top='counts', width=0.5,bottom=0)
  return json.dumps(json_item(p))

@app.route('/histogram1')
def his1():
  import random
  p=figure(title = "histogram", sizing_mode="fixed", plot_width=600, plot_height=400,tools='pan,wheel_zoom,box_zoom,save,reset')
  p.toolbar.logo=None
  p.add_tools(
    HoverTool(tooltips = [('Left Interval', '@left'),
                          ('Right Interval', '@right'),
                          ('count','@arr_hist')
                          ])
  )
  a=np.random.normal(size=10000)
  arr_hist,edges=np.histogram(a, bins = 100, range = [a.min(), a.max()])
  his = pd.DataFrame({'arr_hist': arr_hist, 
                       'left': edges[:-1], 
                       'right': edges[1:]})
  src = ColumnDataSource(his)
  p.quad(source = src, bottom=0, top='arr_hist',
       left='left', right='right', 
       line_color='black')
  return json.dumps(json_item(p))

@app.route('/heatmap')
def heatmap():
  data=pd.DataFrame(
    [ [1,0.2,0.3],
      [0.3,1,0.5],
      [-0.5,0.8,1]],
    columns=['a','b','c'])
  value=[]
  for x in data.apply(tuple):
    value.extend(x)
  absValue=[abs(number) for number in value]
  print(data)
  source={
    'x': [i for i in list(data.columns) for j in list(data.columns)],
    'y': list(data.columns)*len(data.columns),
    'value':value,
    'abs':absValue
  }
  p=figure(title = "heatmap", sizing_mode="fixed", plot_width=600, plot_height=400,tools='pan,wheel_zoom,box_zoom,save,reset',x_range=list(data.columns),y_range=list(reversed(data.columns)))
  p.toolbar.logo=None
  from bokeh.models import LinearColorMapper
  from bokeh.palettes import inferno,YlOrRd,Magma,PuBu,Greys
  from bokeh.transform import transform
  crs=PuBu[9]
  crs.reverse()
  mapper = LinearColorMapper(palette=crs, low=min(absValue), high=max(absValue))
  fontMapper=LinearColorMapper(palette=[Greys[5][0],Greys[5][4]], low=min(absValue), high=max(absValue))
  p.rect(x="x", y="y", width=1, height=1, source=source,
       line_color=None, fill_color=transform('abs', mapper))
  p.text(x="x", y="y",text='value', source=source,text_font_size='2em',text_font_style='bold',text_align='center',text_baseline='middle',text_color=transform('abs',fontMapper))
  p.add_tools(
    HoverTool(tooltips = [('Value', '@value')])
  )
  return json.dumps(json_item(p))

@app.route('/multiline')
def multiline():
  x=[1,2,3,4,5,6,7,8,9,10]
  y1=[5,2,4,8,3,4,8,3,4,6]
  y2=[8,3,7,2,7,5,0,5,0,5]
  data={'x':x,'y1':y1,'y2':y2}
  p=figure(title = "multiline", sizing_mode="fixed", plot_width=600, plot_height=400,tools='pan,wheel_zoom,box_zoom,save,reset')
  p.toolbar.logo=None
  from bokeh.models import LinearColorMapper
  from bokeh.palettes import inferno,YlOrRd,Magma,PuBu,Greys
  from bokeh.transform import transform
  #p.vline_stack(['y1','y2'],x='x',source=data)
  p.multi_line([x,x],[y1,y2],color=['blue','red'])
  p.add_tools(
    HoverTool(tooltips = [('X,Y1,Y2', '@value')])
  )
  return json.dumps(json_item(p))

@app.route('/multiline2')
def multiline2():
  xData={
    "a":[2,5,6,8,9,4,1,10,7,3]
  }
  x=[2,5,6,8,9,4,1,10,7,3]
  ya=[5,2,4,8,3,4,8,3,4,6]
  yb=[4,1,3,7,2,3,7,2,3,5]
  data=ColumnDataSource(data={'x':x,'ya':ya,'yb':yb})
  p=figure(title = "multiline", sizing_mode="fixed", plot_width=600, plot_height=400,tools='pan,wheel_zoom,box_zoom,save,reset')
  p.toolbar.logo=None
  from bokeh.models import LinearColorMapper
  from bokeh.models.glyphs import Line,Circle
  from bokeh.palettes import inferno,YlOrRd,Magma,PuBu,Greys
  from bokeh.transform import transform
  #p.vline_stack(['y1','y2'],x='x',source=data)
  l1=Line(x='x',y='yb',line_color='red',line_width=2)
  l2=Circle(x='x',y='ya',fill_color='blue',fill_alpha=0.4,size=7)
  r1=p.add_glyph(data,l1,name='predict')
  r2=p.add_glyph(data,l2,name='real')

  p.add_tools(
    HoverTool(tooltips = [('X,Y_real', '@x,@ya')],names=['real'])
  )
  p.add_tools(
    HoverTool(tooltips = [('X,Y_predict', '@x,@yb')],names=['predict'])
  )
  from bokeh.models import Button
  from bokeh import events
  callback = CustomJS(args=dict(source=data), code="""
          var data = source.data;
          let newList = [];
          for(var i=0;i<data['x'].length;i++){
            newList.push({
              value1: data['x'][i],
              value2: data['ya'][i],
              value3: data['yb'][i]
            })
          }
          console.log(newList)
          newList.sort(function(a,b) {
            return ((a.value1 - b.value1))
          })
          console.log(newList)
          for(var i=0;i<newList.length;i++){
            data['x'][i]=newList[i].value1
            data['ya'][i]=newList[i].value2
            data['yb'][i]=newList[i].value3
          }
          console.log(data)
          source.change.emit();
      """)

  dp = Button(label="sort")
  dp.js_on_event(events.ButtonClick, callback)
  layout = column(dp, p)
  return json.dumps(json_item(layout))

@app.route('/scatterSelect')
def scatterSelect():
  colormap = {'0': 'red', '1': 'green', 'virginica': 'blue'}
  a=[1,2,3,4,5,6,7,8,9]
  b=[2,3,4,5,6,7,8,9,10]
  c=[2,5,6,8,9,7,2,2,4]
  d=['red','green','green','blue','red','green','green','blue','green']
  source=ColumnDataSource(data={'a':a,'b':b,'c':c,'d':d,'x':a,'y':b,'color':d})
  p=figure(title = "x-y", sizing_mode="fixed", plot_width=600, plot_height=400,tools='pan,wheel_zoom,box_zoom,save,reset')
  p.toolbar.logo=None
  p.add_tools(
    HoverTool(
      show_arrow=True, 
      line_policy='next',
      tooltips=[
          ('X_value', '$data_x'),
          ('Y_value', '$data_y')
      ]
    )
  )
  p.scatter(x='x',y='y', color='color',source=source)
  from bokeh.layouts import column,row
  from bokeh.models import Dropdown
  callback1 = CustomJS(args=dict(source=source,axis=p.xaxis[0]), code="""
          var data = source.data;
          var f = cb_obj.value
          data['x']=data[f]
          axis.axis_label=f
          source.change.emit();
      """)
  callback2 = CustomJS(args=dict(source=source,axis=p.yaxis[0]), code="""
          var data = source.data;
          var f = cb_obj.value
          data['y']=data[f]
          axis.axis_label=f
          source.change.emit();
      """)

  dp1 = Dropdown(label="X value",menu=[('aa','a'),('bb','b'),('cc','c')],default_value='b')
  dp1.js_on_change('value', callback1)
  dp2 = Dropdown(label="Y value",menu=['a','b','c'],default_value='b')
  dp2.js_on_change('value', callback2)
  layout = column(row(dp1,dp2), p)

  return json.dumps(json_item(layout))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8787)