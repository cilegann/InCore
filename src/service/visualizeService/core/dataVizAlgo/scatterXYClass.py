from service.visualizeService.core.dataVizBase import dataViz
from bokeh.models import HoverTool,ColumnDataSource
from bokeh.palettes import Category20,Category10
from random import shuffle
import pandas as pd
import logging
from service.analyticService.core.preprocessCore.missingFiltering import missingFiltering

class scatterXYClass(dataViz):
    def __init__(self,algoInfo,dataCol,fid):
        super().__init__(algoInfo,dataCol,fid)

    def doBokehViz(self):
        try:
            self.bokeh_fig.xaxis.axis_label = self.dataCol['x']
            self.bokeh_fig.yaxis.axis_label = self.dataCol['y']
            [x,y,c]=missingFiltering().filtCols([self.data['x'],self.data['y'],self.data['value']],['float','float',self.colTypes[self.dataCol['value']]],[True,True,True])
            if len(set(c))>9:
                cmap=Category20[20]
            else:
                cmap=Category10[10]
            cateMapping={str(k):i for i,k in enumerate(list(set(c)))}
            color=[cmap[cateMapping[str(k)]] for k in c]
            # shuffle(cmap)
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
            self.bokeh_fig.scatter('x','y',source=source, color='color' , size=5,legend='class')
        except Exception as e:
            raise Exception(f'[{self.algoInfo["algoname"]}][do_bokeh_viz] {e}')
