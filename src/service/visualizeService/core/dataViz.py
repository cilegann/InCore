from bokeh.embed import json_item,components
from bokeh.plotting import figure
from bokeh.models import CustomJS,SaveTool,Tool,CustomAction,HoverTool,CustomJSHover,ColumnDataSource
import pandas as pd

from service.dataService.utils import getFileInfo,getDf

class dataViz():
    def __init__(self,algoInfo,dataCol,fid):
        self.fid=fid
        self.algoInfo=algoInfo
        self.dataCol=dataCol #{"x":"x_col","y":"y_col","value":"value_col"}
        self.data=self.getData()
        self.figure=self.init_figure()
        self.imgId=""
        self.img=None
        self.done=False
        self.errorMsg=""

    def getData(self):
        fileInfo=getFileInfo(self.fid)
        if fileInfo['status']!='success':
            raise Exception("[GetFileInfo] error:"+str(fileInfo['msg']))
        fileInfo=fileInfo['data'][0]
        filepath=fileInfo[2]
        if fileInfo[3]!=None:
            filepath=fileInfo[3]
        
        

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