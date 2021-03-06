from service.visualizeService.core.dataVizBase import dataViz
from bokeh.models import HoverTool
from service.analyticService.core.preprocessCore.missingFiltering import missingFiltering

class lineXY(dataViz):
    def __init__(self,algoInfo,dataCol,fid):
        super().__init__(algoInfo,dataCol,fid)

    def doBokehViz(self):
        try:
            self.bokeh_fig.xaxis.axis_label = self.dataCol['x']
            self.bokeh_fig.yaxis.axis_label = self.dataCol['y']
            [x,y]=missingFiltering().filtCols([self.data['x'],self.data['y']],['float','float'],[True,True])
            x,y=zip(*sorted(zip(x,y)))
            x=list(x)
            y=list(y)
            self.bokeh_fig.add_tools(
                HoverTool(
                    show_arrow=True, 
                    line_policy='next',
                    tooltips=[
                        ('X_value', '$data_x'),
                        ('Y_value', '$data_y')
                    ]
                )
            )
            self.bokeh_fig.line(x,y)
        except Exception as e:
            raise Exception(f'[{self.algoInfo["algoname"]}][do_bokeh_viz]{e}')
