from service.visualizeService.core.dataVizBase import dataViz
from bokeh.models import HoverTool,ColumnDataSource
from service.analyticService.core.preprocessAlgo.missingFiltering import missingFiltering
from bokeh.models.glyphs import Line,Circle
from bokeh.layouts import column,row
from bokeh.models import Dropdown,CustomJS

class dotLineSelect(dataViz):
    '''
    data={ "x":np.array, "y_dot":np.array, "y_line":np.array }
    colName={"x":"x axis name", "y":"y axis name"}
    '''
    def __init__(self,xData,dotData,lineData,w=625,h=400):
        try:
            self.algoInfo={}
            self.algoInfo['lib']='bokeh'
            self.algoInfo['friendlyname']=""
            self.algoInfo['algoname']='dotLineSelect'
            self.xData=xData
            self.dotData=dotData
            self.lineData=lineData
            self.bokeh_fig=self.init_figure(w=w,h=h)
            self.component=None
        except Exception as e:
            raise Exception(f'[analyticViz][{self.algoInfo["algoname"]}]{e}')
    def doBokehViz(self):
        try:
            #[x,y_dot,y_line]=missingFiltering().filtCols([self.data['x'],self.data['y_dot'],self.data['y_line']],['float','float','float'],[True,True,True])
            # x,y_dot,y_line=zip(*sorted(zip(x,y_dot,y_line)))
            # x=list(x)
            # y_dot=list(y_dot)
            # y_line=list(y_line)
            dic={}
            x_menu=[]
            y_menu=[]
            for k,v in self.xData.items():
                dic['x_'+k]=v
                x_menu.append(k)
            for k,v in self.dotData.items():
                dic['dot_'+k]=v
                dic['line_'+k]=self.lineData[k]
                y_menu.append(k)
            x,y_dot,y_line=zip(*sorted(zip(self.xData[x_menu[0]],self.dotData[y_menu[0]],self.lineData[y_menu[0]])))
            x=list(x)
            y_dot=list(y_dot)
            y_line=list(y_line)
            dic['_bokeh_to_plot_x']=x
            dic['_bokeh_to_plot_dot']=y_dot
            dic['_bokeh_to_plot_line']=y_line
            data=ColumnDataSource(data=dic)
            self.bokeh_fig.xaxis.axis_label=x_menu[0]
            self.bokeh_fig.xaxis.axis_label=x_menu[1]
            l1=Line(x='_bokeh_to_plot_x',y='_bokeh_to_plot_line',line_color='red',line_width=2)
            l2=Circle(x='_bokeh_to_plot_x',y='_bokeh_to_plot_dot',fill_color='blue',fill_alpha=0.4,size=7)
            r1=self.bokeh_fig.add_glyph(data,l1,name='line')
            r2=self.bokeh_fig.add_glyph(data,l2,name='dot')
            self.bokeh_fig.add_tools(
                HoverTool(tooltips = [('X,Y', '@_bokeh_to_plot_x,@_bokeh_to_plot_dot')],names=['dot'])
            )
            self.bokeh_fig.add_tools(
                HoverTool(tooltips = [('X,Y', '@_bokeh_to_plot_x,@_bokeh_to_plot_line')],names=['line'])
            )
            #TODO: sort by X
            # add a list to datasource, imply the origin index after sorting
            callbackX = CustomJS(args=dict(source=data,axis=self.bokeh_fig.xaxis[0]), code="""
                    var data = source.data;
                    var f = cb_obj.value
                    data['_bokeh_to_plot_x']=data['x_'+f]
                    axis.axis_label=f
                    source.change.emit();
                """)
            callbackY = CustomJS(args=dict(source=data,axis=self.bokeh_fig.yaxis[0]), code="""
                    var data = source.data;
                    var f = cb_obj.value
                    data['_bokeh_to_plot_dot']=data['dot_'+f]
                    data['_bokeh_to_plot_line']=data['line_'+f]
                    axis.axis_label=f
                    source.change.emit();
                """)

            dp1 = Dropdown(label="X value",menu=x_menu,default_value=x_menu[0])
            dp1.js_on_change('value', callbackX)
            dp2 = Dropdown(label="Y value",menu=y_menu,default_value=y_menu[0])
            dp2.js_on_change('value', callbackY)
            self.bokeh_fig = column(row(dp1,dp2), self.bokeh_fig)
        except Exception as e:
            raise Exception(f'[{self.algoInfo["algoname"]}][do_bokeh_viz]{e}')
        
