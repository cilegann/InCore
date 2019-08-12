from service.visualizeService.core.dataViz import dataViz
from bokeh.models import HoverTool

class circleXY(dataViz):
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
            self.bokeh_fig.circle(self.data['x'],self.data['y'], fill_alpha=0.2, size=10)
        except Exception as e:
            raise Exception(f'[{self.algoInfo["algoname"]}][do_bokeh_viz] {e}')
