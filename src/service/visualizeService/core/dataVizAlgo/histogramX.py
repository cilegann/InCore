from service.visualizeService.core.dataViz import dataViz
from bokeh.models import HoverTool,Range1d,ColumnDataSource
import pandas as pd
import numpy as np
from service.analyticService.core.preprocess.missingFiltering import missingFiltering

class histogramX(dataViz):
    def __init__(self,algoInfo,dataCol,fid):
        super().__init__(algoInfo,dataCol,fid)

    def doBokehViz(self):
        try:
            [x]=missingFiltering().filtCols([self.data['x']],['float'],[True])
            arr_hist,edges=np.histogram(x, bins = 100, range = [x.min(), x.max()])
            his = pd.DataFrame({'arr_hist': arr_hist, 
                       'left': edges[:-1], 
                       'right': edges[1:]})
            src = ColumnDataSource(his)
            self.bokeh_fig.add_tools(
                HoverTool(
                    show_arrow=True, 
                    line_policy='next',
                    tooltips = [('Left bound', '@left'),
                                        ('Right bound', '@right'),
                                        ('count','@arr_hist')
                    ]
                )
            )
            self.bokeh_fig.quad(source = src, bottom=0, top='arr_hist',
                                left='left', right='right', 
                                line_color='black')
        except Exception as e:
            raise Exception(f'[{self.algoInfo["algoname"]}][do_bokeh_viz]{e}')
