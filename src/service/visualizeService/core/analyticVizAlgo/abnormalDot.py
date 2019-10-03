from service.visualizeService.core.dataVizAlgo.circleXYClass import circleXYClass
from bokeh.models import HoverTool,ColumnDataSource
from bokeh.models import CustomJS,Select
from bokeh.layouts import column,row

class abnormalDot(circleXYClass):
    '''
    @data =
        {
            "x_col_1": 1D np.array,
            "x_col_2": 1D np.array,
            ...
        }
    @categ= 1D np.array of -1 and 1
    '''
    def __init__(self,data,categ,figName,w=625,h=350):
        try:
            self.algoInfo={}
            self.algoInfo['lib']='bokeh'
            self.algoInfo['friendlyname']=figName
            self.algoInfo['algoname']='abnormalDot'
            self.data=data
            self.categ=categ
            self.bokeh_fig=self.init_figure(w=w,h=h)
            self.component=None
        except Exception as e:
            raise Exception(f'[analyticViz][{self.algoInfo["algoname"]}]{e}')
    def doBokehViz(self):
        try:
            dic=self.data
            menus=[k for k in dic]
            colors=[]
            for c in self.categ:
                if c==1:
                    colors.append('black')
                elif c==-1:
                    colors.append('red')
            dic['categ']=colors
            dic['bokeh_plt_x']=dic[menus[0]]
            if len(menus)==1:
                dic['bokeh_plt_y']=dic[menus[0]]
            else:   
                dic['bokeh_plt_y']=dic[menus[1]]
            data=ColumnDataSource(dic)
            self.bokeh_fig.xaxis.axis_label=menus[0]
            if len(menus)==1:
                self.bokeh_fig.yaxis.axis_label=menus[0]
            else:
                self.bokeh_fig.yaxis.axis_label=menus[1]
            self.bokeh_fig.circle('bokeh_plt_x','bokeh_plt_y',source=data,color='categ',fill_alpha=0.2,size=10)
            self.bokeh_fig.add_tools(
                HoverTool(tooltips = [('X,Y', '@bokeh_plt_x,@bokeh_plt_y')])
            )
            callbackX = CustomJS(args=dict(source=data,axis=self.bokeh_fig.xaxis[0]), code="""
                        var data=source.data
                        var f = cb_obj.value
                        data['bokeh_plt_x']=data[f]
                        axis.axis_label=f
                        source.change.emit();
                    """)
            callbackY = CustomJS(args=dict(source=data,axis=self.bokeh_fig.yaxis[0]), code="""
                        var data=source.data
                        var f = cb_obj.value
                        data['bokeh_plt_y']=data[f]
                        axis.axis_label=f
                        source.change.emit();
                """)

            #dp1 = Dropdown(label="X value",menu=x_menu,default_value=x_menu[0])
            dp1=Select(title="X-coordinate:",value=menus[0],options=menus)
            dp1.js_on_change('value', callbackX)
            #dp2 = Dropdown(label="Y value",menu=y_menu,default_value=y_menu[0])
            if len(menus)==1:
                dp2=Select(title="Y-coordinate:",value=menus[0],options=menus)
            else:
                dp2=Select(title="Y-coordinate:",value=menus[1],options=menus)
            dp2.js_on_change('value', callbackY)
            self.bokeh_fig = column(row(dp1,dp2), self.bokeh_fig)
        except Exception as e:
            raise Exception(f'[{self.algoInfo["algoname"]}][do_bokeh_viz]{e}')