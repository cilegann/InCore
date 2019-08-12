from bokeh.embed import json_item,components
from bokeh.plotting import figure
from bokeh.models import CustomJS,SaveTool,Tool,CustomAction,HoverTool,CustomJSHover,ColumnDataSource
import pandas as pd
import numpy as np
from PIL import Image
from datetime import date
import uuid
from params import params
from service.dataService.utils import getFileInfo,getDf
from utils import sql
import logging
import json

class dataViz():
    def __init__(self,algoInfo,dataCol,fid):
        try:
            self.params=params()
            self.imgId=str(uuid.uuid1())
            self.fid=fid
            self.algoInfo=algoInfo
            self.dataCol=dataCol #{"x":"x_col","y":"y_col","value":"value_col"}
            self.data=self.getData() #{"x":np.array,"y":np.array,"all":np.array,"value":np.array}
            self.bokeh_fig=self.init_figure()
            self.imgWH=None
            self.mat_plt=None
            self.component=None
            logging.debug(f'[dataViz] algoInfo: {self.algoInfo}')
        except Exception as e:
            raise Exception(f'[dataViz][{self.algoInfo["algoname"]}]{e}')
        

    def getData(self):
        fileInfo=getFileInfo(self.fid)
        try:
            fileInfo=getFileInfo(self.fid)
            if len(fileInfo)==0:
                raise Exception(f'fileUid not found')
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
            raise Exception(f'[getData] {e}')
            
        return data
        

    def init_figure(self):
        try:
            if self.algoInfo['lib']=='bokeh':
                p = figure(title = self.algoInfo['friendlyname'], sizing_mode="fixed", plot_width=625, plot_height=400,tools='pan,wheel_zoom,box_zoom,reset,save')
            else:
                p = figure(title = self.algoInfo['friendlyname'], sizing_mode="fixed", plot_width=625, plot_height=400,tools='pan,wheel_zoom,box_zoom,reset')
                saveCallback=CustomJS(code=f"""window.open('http://{self.params.host}:{self.params.port}/viz/getimg/?uid={self.imgId}&action=download');""")
                p.add_tools(CustomAction(icon="./icons/save_icon.png",callback=saveCallback))
                p.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
                p.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
                p.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
                p.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks
                p.xaxis.major_label_text_font_size = '0pt'  # turn off x-axis tick labels
                p.yaxis.major_label_text_font_size = '0pt'  # turn off y-axis tick labels
            p.toolbar.logo=None
        except Exception as e:
            raise Exception(f'[initFig] {e}')
        return p

    def doBokehViz(self):
        '''
        implement in each algo
        0. the bokeh figure is self.bokeh_fig
        1. set self.bokeh_fig.xaxis.axis_label using self.dataCol['x']
        2. set self.bokeh_fig.yaxis.axis_label using self.dataCol['y']
        3. implement bokeh algorithm using self.data['x'], self.data['y'], self.data['all']
        4. add hovertool if necessary
        5. ***** DONT'T save or show anything! *****
        '''
        raise Exception(f' do_bokeh_viz not implemented')


    def doMatpltViz(self):
        '''
        implement in each algo
        0. the matplotlib plt is self.mat_plt
        1. set xaxis name using self.dataCol['x']
        2. set yaxis name using self.dataCol['y']
        3. implement matplotlib algorithm using self.data['x'], self.data['y'], self.data['all']
        4. ***** DONT'T save or show anything! *****
        '''
        raise Exception(f' do_matplt_viz not implemented')


    def saveimg(self):
        try:
            self.mat_plt.savefig(f'{self.params.imgpath}/{self.imgId}.png', dpi=300,bbox_inches='tight')
            self.imgWH=Image.open(f'{self.imgId}.png').size
            td=date.today()
            db=sql()
            db.cursor.execute(f"INSERT INTO `incore`.`plottedImgs` (`id`, `path`, `width`, `height`, `createdTime`) VALUES ('{self.imgId}', '{self.params.imgpath}/{self.imgId}.png', '{self.imgWH[0]}', '{self.imgWH[1]}', '{td.year}-{td.month}-{td.day}');")
            db.conn.commit()
        except Exception as e:
            raise Exception(f'[saveImg] {e}')
        finally:
            db.conn.close()

    def img2bokeh(self):
        try:
            self.bokeh_fig.image_url(url=[f"http://{self.params.host}:{self.params.port}/viz/getimg/?uid={self.imgId}&action=get"], x=0, y=0, w=self.imgWH[0], h=self.imgWH[1],anchor='bottom_left')
        except Exception as e:
            raise Exception(f'[img2bokeh] {e}')

    def getComp(self):
        try:
            script,div=components(self.bokeh_fig,wrap_script=False)
            self.component=({"div":div,"script":script})
        except Exception as e:
            raise Exception(f'[getData] {e}')