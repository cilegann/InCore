from service.visualizeService.core.dataVizBase import dataViz
from bokeh.models import HoverTool,Range1d,ColumnDataSource,FactorRange
import pandas as pd
from bokeh.plotting import figure
from service.analyticService.core.preprocessCore.missingFiltering import missingFiltering

class barCnt(dataViz):
    def __init__(self,algoInfo,dataCol,fid):
        super().__init__(algoInfo,dataCol,fid)

    def init_figure(self,w=625,h=400):
        try:
            if self.algoInfo['lib']=='bokeh':
                p = figure(title = self.algoInfo['friendlyname'], sizing_mode="fixed", plot_width=w, plot_height=h,tools='pan,wheel_zoom,box_zoom,reset,save',x_range=FactorRange(["1","2"]))
            p.toolbar.logo=None
        except Exception as e:
            raise Exception(f'[initFig] {e}')
        return p

    def doBokehViz(self):
        try:
            [c]=missingFiltering().filtCols([self.data['x']],['int'],[True])
            cnt=[[str(x),list(c).count(x)] for x in set(c)]
            self.bokeh_fig.x_range.factors=[d[0] for d in cnt]#Range1d(min(c)-1,max(c)+1)
            self.bokeh_fig.xaxis.axis_label = "class"
            self.bokeh_fig.yaxis.axis_label = "count"
            source = ColumnDataSource(pd.DataFrame({'counts':[d[1] for d in cnt],'class':[d[0] for d in cnt]}) )
            self.bokeh_fig.add_tools(
                HoverTool(
                    show_arrow=True, 
                    line_policy='next',
                    tooltips=[
                        ('class','@class'),
                        ('count', '@counts')
                        
                    ]
                )
            )
            self.bokeh_fig.vbar(source=source,x='class', top='counts', width=0.7,bottom=0)
        except Exception as e:
            raise Exception(f'[{self.algoInfo["algoname"]}][do_bokeh_viz]{e}')
