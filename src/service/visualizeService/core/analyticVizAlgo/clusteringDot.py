from service.visualizeService.core.dataVizAlgo.circleXYClass import circleXYClass
from bokeh.models import HoverTool,ColumnDataSource
from bokeh.models import CustomJS,Select
from bokeh.layouts import column,row
from bokeh.palettes import Category20,Category10

class clusteringDot(circleXYClass):
    '''
    @data =
        {
            "x_col_1": 1D np.array,
            "x_col_2": 1D np.array,
            ...
        }
    @categ= 1D np.array
    '''
    def __init__(self,data,cluster,figName,w=625,h=320):
        try:
            self.algoInfo={}
            self.algoInfo['lib']='bokeh'
            self.algoInfo['friendlyname']=figName
            self.algoInfo['algoname']='clusteringDot'
            self.data=data
            self.cluster=cluster
            self.bokeh_fig=self.init_figure(w=w,h=h)
            self.component=None
        except Exception as e:
            raise Exception(f'[analyticViz][{self.algoInfo["algoname"]}]{e}')
    def doBokehViz(self):
        try:
            dic=self.data
            dic['cluster']=self.cluster
            menus=[k for k in dic]
            colors=[]
            if len(set(self.cluster))>9:
                cmap=Category20[20]
            else:
                cmap=Category10[10]
            colors=[cmap[c] for c in self.cluster]
            dic['categ']=colors
            dic['bokeh_plt_x']=dic[menus[0]]
            if len(menus)>1:
                dic['bokeh_plt_y']=dic[menus[1]]
            else:
                dic['bokeh_plt_y']=dic[menus[0]]
            data=ColumnDataSource(dic)
            self.bokeh_fig.xaxis.axis_label=menus[0]
            if len(menus)>1:
                self.bokeh_fig.yaxis.axis_label=menus[1]
            else:
                self.bokeh_fig.yaxis.axis_label=menus[0]
            self.bokeh_fig.circle('bokeh_plt_x','bokeh_plt_y',source=data,color='categ',fill_alpha=0.2,size=10)
            self.bokeh_fig.add_tools(
                HoverTool(tooltips = [('X,Y,Class', '@bokeh_plt_x,@bokeh_plt_y,@cluster')])
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
            if len(menus)>1:
                dp2=Select(title="Y-coordinate:",value=menus[1],options=menus)
            else:
                dp2=Select(title="Y-coordinate:",value=menus[0],options=menus)
            dp2.js_on_change('value', callbackY)
            self.bokeh_fig = column(row(dp1,dp2), self.bokeh_fig)
        except Exception as e:
            raise Exception(f'[{self.algoInfo["algoname"]}][do_bokeh_viz]{e}')