from service.visualizeService.core.dataViz import dataViz
from bokeh.models import HoverTool

class lineXY(dataViz):
    def __init__(self,algoInfo,dataCol,fid):
        super().__init__(algoInfo,dataCol,fid)

    def doBokehViz(self):
        try:
            self.bokeh_fig.xaxis.axis_label = self.dataCol['x']
            self.bokeh_fig.yaxis.axis_label = self.dataCol['y']
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
            self.bokeh_fig.line(self.data['x'],self.data['y'])
        except Exception as e:
            raise Exception(f'[dataViz][{self.algoInfo["algoname"]}][do_bokeh_viz] {e}')
