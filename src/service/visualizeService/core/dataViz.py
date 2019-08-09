from bokeh.embed import json_item,components
from bokeh.plotting import figure
from bokeh.models import CustomJS,SaveTool,Tool,CustomAction,HoverTool,CustomJSHover,ColumnDataSource
import pandas as pd
import numpy as np
from params import params

from service.dataService.utils import getFileInfo,getDf

class dataViz():
    def __init__(self,algoInfo,dataCol,fid):
        self.fid=fid
        self.algoInfo=algoInfo
        self.dataCol=dataCol #{"x":"x_col","y":"y_col","value":"value_col"}
        self.data=self.getData() #{"x":np.array,"y":np.array,"all":np.array,"value":np.array}
        self.figure=self.init_figure()
        self.imgId=""
        self.img=None
        self.done=False
        self.errorMsg=""
        self.params=params()

    def getData(self):
        fileInfo=getFileInfo(self.fid)
        try:
            fileInfo=getFileInfo(self.fid)
        except Exception as e:
            raise Exception(f'[dataViz][{self.algoInfo["name"]}][getData] {e}')
        fileInfo=fileInfo[0]

        filepath=fileInfo[2]
        if fileInfo[3]!=None:
            filepath=fileInfo[3]
        data={}
        try:
            rawdata=getDf(filepath,fileInfo[1]).get()
        except Exception as e:
            raise Exception(f'[dataViz][{self.algoInfo["name"]}][getData] {e}')
        try:
            data['all']=np.asarray([rawdata[c] for c in rawdata.columns.tolist()])
            if 'x' in self.dataCol:
                data['x']=np.asarray(rawdata[self.dataCol['x']])
            if 'y' in self.dataCol:
                data['y']=np.asarray(rawdata[self.dataCol['y']])
            if 'value' in self.dataCol:
                data['value']=np.asarray(rawdata[self.dataCol['value']])
        except Exception as e:
            raise Exception(f'[dataViz][{self.algoInfo["name"]}][getData] {e}')
            
        return data
        

    def init_figure(self):
        if self.algoInfo['lib']!='bokeh':
            p = figure(title = self.algoInfo['name'], sizing_mode="fixed", plot_width=625, plot_height=400,tools='pan,wheel_zoom,box_zoom,reset,save')
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
        else:
            p = figure(title = self.algoInfo['name'], sizing_mode="fixed", plot_width=625, plot_height=400,tools='pan,wheel_zoom,box_zoom,reset')
            saveCallback=CustomJS(code=f"""window.open('http://{self.params.host}:{self.params.port}/viz/downloadImg/{self.imgId}.png');""")
            p.add_tools(CustomAction(icon="save_icon.png",callback=saveCallback))
            p.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
            p.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
            p.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
            p.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks
            p.xaxis.major_label_text_font_size = '0pt'  # turn off x-axis tick labels
            p.yaxis.major_label_text_font_size = '0pt'  # turn off y-axis tick labels
        p.toolbar.logo=None

    def do_bokeh_viz(self):
        #run visualization
        pass

    def do_matplt_viz(self):
        pass

    def saveimg(self):
        pass

    def img2bokeh(self):
        pass

    def returnComp(self):

        pass