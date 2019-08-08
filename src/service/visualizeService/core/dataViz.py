from bokeh.embed import json_item,components
from bokeh.plotting import figure
from bokeh.models import CustomJS,SaveTool,Tool,CustomAction,HoverTool,CustomJSHover,ColumnDataSource
import pandas as pd
import numpy as np

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

    def getData(self):
        try:
            fileInfo=getFileInfo(self.fid)
        except Exception as e:
            raise Exception(f'[dataViz]{self.algoInfo["name"]}[getData]{e}')
        fileInfo=fileInfo[0]

        filepath=fileInfo[2]
        if fileInfo[3]!=None:
            filepath=fileInfo[3]
        data={}
        try:
            rawdata=getDf(filepath,fileInfo[1])
        except Exception as e:
            raise Exception(f'[dataViz]{self.algoInfo["name"]}[getData]{e}')
        data['all']=rawdata
        if 'x' in self.dataCol:
            data['x']=np.asarray(rawdata[self.dataCol['x']])
        if 'y' in self.dataCol:
            data['y']=np.asarray(rawdata[self.dataCol['y']])
        if 'value' in self.dataCol:
            data['value']=np.asarray(rawdata[self.dataCol['value']])
        return data
        

    def init_figure(self):
        #initial a bokeh figure instance
        pass

    def getData(self):
        #put dataframe into self.data according to paramSet
        pass

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