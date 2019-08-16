from service.visualizeService.core.dataViz import dataViz
from bokeh.models import HoverTool,ColumnDataSource
from bokeh.palettes import Category20,Category10
from random import shuffle
import pandas as pd
import logging
from service.analyticService.core.preprocess.missingFiltering import missingFiltering

class circleXYClass(dataViz):
    def __init__(self,algoInfo,dataCol,fid):
        super().__init__(algoInfo,dataCol,fid)

    def doBokehViz(self):
        try:
            self.bokeh_fig.xaxis.axis_label = self.dataCol['x']
            self.bokeh_fig.yaxis.axis_label = self.dataCol['y']
            [x,y,c]=missingFiltering().filtCols([self.data['x'],self.data['y'],self.data['value']],['float','float','int'],[True,True,True])
            
            if max(c)>9:
                cmap=Category20[20]
            else:
                cmap=Category10[10]
            # shuffle(cmap)
            color=[cmap[i] for i in c]
            source=ColumnDataSource(pd.DataFrame({'x':x,'y':y,'class':c,'color':color}))
            self.bokeh_fig.add_tools(
                HoverTool(
                    show_arrow=True, 
                    line_policy='next',
                    tooltips=[
                        ('X_value', '$data_x'),
                        ('Y_value', '$data_y'),
                        ('class','@class')
                    ]
                )
            )
            self.bokeh_fig.circle('x','y',source=source, color='color' ,fill_alpha=0.2, size=10)
        except Exception as e:
            raise Exception(f'[{self.algoInfo["algoname"]}][do_bokeh_viz] {e}')
