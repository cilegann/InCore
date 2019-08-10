from bokeh.embed import json_item,components
from bokeh.plotting import figure
from bokeh.models import CustomJS,SaveTool,Tool,CustomAction,HoverTool,CustomJSHover,ColumnDataSource
import pandas as pd
import numpy as np
from params import params
from PIL import Image
from datetime import date
import uuid

from service.dataService.utils import getFileInfo,getDf
from utils import sql

class dataViz():
    def __init__(self,algoInfo,dataCol,fid):
        self.fid=fid
        self.algoInfo=algoInfo
        self.dataCol=dataCol #{"x":"x_col","y":"y_col","value":"value_col"}
        self.data=self.getData() #{"x":np.array,"y":np.array,"all":np.array,"value":np.array}
        self.bokeh_fig=self.init_figure()
        self.imgId=str(uuid.uuid1())
        self.imgWH=None
        self.plt_fig=None
        self.params=params()

    def getData(self):
        fileInfo=getFileInfo(self.fid)
        try:
            fileInfo=getFileInfo(self.fid)
            fileInfo=fileInfo[0]
            filepath=fileInfo[2]
            if fileInfo[3]!=None:
                filepath=fileInfo[3]
            data={}

            rawdata=getDf(filepath,fileInfo[1]).get()

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
        try:
            if self.algoInfo['lib']!='bokeh':
                p = figure(title = self.algoInfo['name'], sizing_mode="fixed", plot_width=625, plot_height=400,tools='pan,wheel_zoom,box_zoom,reset,save')
            else:
                p = figure(title = self.algoInfo['name'], sizing_mode="fixed", plot_width=625, plot_height=400,tools='pan,wheel_zoom,box_zoom,reset')
                saveCallback=CustomJS(code=f"""window.open('http://{self.params.host}:{self.params.port}/viz/getimg/?uid={self.imgId}&action=download');""")
                p.add_tools(CustomAction(icon="save_icon.png",callback=saveCallback))
                p.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
                p.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
                p.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
                p.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks
                p.xaxis.major_label_text_font_size = '0pt'  # turn off x-axis tick labels
                p.yaxis.major_label_text_font_size = '0pt'  # turn off y-axis tick labels
            p.toolbar.logo=None
        except Exception as e:
            raise Exception(f'[dataViz][{self.algoInfo["name"]}][initFig] {e}')
        return p

    def do_bokeh_viz(self):
        #implement in algo
        pass

    def do_matplt_viz(self):
        #implement in algo
        pass

    def saveimg(self):
        try:
            self.mat_plt.savefig(f'{self.params.imgpath}/{self.imgId}.png', dpi=300,bbox_inches='tight')
            self.imgWH=Image.open(f'{self.imgId}.png').size
            td=date.today()
            db=sql()
            db.cursor.execute(f"INSERT INTO `incore`.`plottedImgs` (`id`, `path`, `width`, `height`, `createdTime`) VALUES ('{self.imgId}', '{self.params.imgpath}/{self.imgId}.png', '{self.imgWH[0]}', '{self.imgWH[1]}', '{td.year}-{td.month}-{td.day}');")
            db.conn.commit()
        except Exception as e:
            raise Exception(f'[dataViz][{self.algoInfo["name"]}][saveImg] {e}')
        finally:
            db.conn.close()

    def img2bokeh(self):
        try:
            self.bokeh_fig.image_url(url=[f"http://{self.params.host}:{self.params.port}/viz/getimg/?uid={self.imgId}&action=get"], x=0, y=0, w=1200, h=675,anchor='bottom_left')
        except Exception as e:
            raise Exception(f'[dataViz][{self.algoInfo["name"]}][img2bokeh] {e}')

    def returnComp(self):
        script,div=components(self.bokeh_fig,wrap_script=False)
        response=make_response(json.dumps({"div":div,"script":script}))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response