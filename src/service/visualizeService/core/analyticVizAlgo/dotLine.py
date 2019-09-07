from service.visualizeService.core.dataVizBase import dataViz
from bokeh.models import HoverTool,ColumnDataSource
from service.analyticService.core.preprocessAlgo.missingFiltering import missingFiltering
from bokeh.models.glyphs import Line,Circle

class dotLine(lineXY):
    '''
    data={ "x":np.array, "y_dot":np.array, "y_line":np.array }
    colName={"x":"x axis name", "y":"y axis name"}
    '''
    def __init__(self,data,colName,figName,w=625,h=400):
        try:
            self.algoInfo={}
            self.algoInfo['lib']='bokeh'
            self.algoInfo['friendlyname']=figName
            self.algoInfo['algoname']='multiLine'
            self.data=data
            self.dataCol={}
            self.bokeh_fig=self.init_figure(w=w,h=h)
            self.component=None
        except Exception as e:
            raise Exception(f'[analyticViz][{self.algoInfo["algoname"]}]{e}')
    def doBokehViz(self):
        try:
            # self.bokeh_fig.xaxis.axis_label = self.dataCol['x']
            # self.bokeh_fig.yaxis.axis_label = self.dataCol['y']
            [x,y_dot,y_line]=missingFiltering().filtCols([self.data['x'],self.data['y_dot'],self.data['y_line']],['float','float','float'],[True,True,True])
            x,y_dot,y_line=zip(*sorted(zip(x,y_dot,y_line)))
            x=list(x)
            y_dot=list(y_dot)
            y_line=list(y_line)
            data=ColumnDataSource(data={'x':x,'y_dot':y_dot,'y_line':y_line})
            l1=Line(x='x',y='y_line',line_color='red',line_width=2)
            l2=Circle(x='x',y='y_dot',fill_color='blue',fill_alpha=0.4,size=7)
            r1=self.bokeh_fig.add_glyph(data,l1,name='line')
            r2=self.bokeh_fig.add_glyph(data,l2,name='dot')

            self.bokeh_fig.add_tools(
                HoverTool(tooltips = [('X,Y', '@x,@y_dot')],names=['dot'])
            )
            self.bokeh_fig.add_tools(
                HoverTool(tooltips = [('X,Y', '@x,@y_line')],names=['line'])
            )
        except Exception as e:
            raise Exception(f'[{self.algoInfo["algoname"]}][do_bokeh_viz]{e}')
        
