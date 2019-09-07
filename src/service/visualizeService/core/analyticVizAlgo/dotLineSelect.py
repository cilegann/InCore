from service.visualizeService.core.dataVizBase import dataViz
from bokeh.models import HoverTool,ColumnDataSource
from service.analyticService.core.preprocessAlgo.missingFiltering import missingFiltering
from bokeh.models.glyphs import Line,Circle
from bokeh.layouts import column,row
from bokeh.models import Dropdown,CustomJS,Select,Legend,LegendItem

class dotLineSelect(dataViz):
    '''
    @xData =
        {
            "x_col_1": 1D np.array,
            "x_col_2": 1D np.array,
            ...
        }
    @dotData =
        {
            "y_col_1": 1D np.array,
            "y_col_2": 1D np.array,
            ...
        }
    @lineData = 
        {
            "y_col_1": 1D np.array,
            "y_col_2": 1D np.array,
            ...
        }
    @dot = "legend name of dot"
    @line = "legend name of dot"
    
    *** Notice: 
        1. dotData and lineData should contain same keys
        2. for the np.array, their length must be the same
    '''
    def __init__(self,xData,dotData,lineData,dotName="real",lineName="predict",w=625,h=400):
        try:
            self.algoInfo={}
            self.algoInfo['lib']='bokeh'
            self.algoInfo['friendlyname']=""
            self.algoInfo['algoname']='dotLineSelect'
            self.xData=xData
            self.dotData=dotData
            self.lineData=lineData
            self.dotName=dotName
            self.lineName=lineName
            self.bokeh_fig=self.init_figure(w=w,h=h)
            self.component=None
        except Exception as e:
            raise Exception(f'[analyticViz][{self.algoInfo["algoname"]}]{e}')
    def doBokehViz(self):
        try:
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
            index=[i for i in range(len(self.xData[x_menu[0]]))]
            x,y_dot,y_line,index=zip(*sorted(zip(self.xData[x_menu[0]],self.dotData[y_menu[0]],self.lineData[y_menu[0]],index)))
            x=list(x)
            y_dot=list(y_dot)
            y_line=list(y_line)
            index=list(index)
            dic['_bokeh_to_plot_x']=x
            dic['_bokeh_to_plot_dot']=y_dot
            dic['_bokeh_to_plot_line']=y_line
            dic['_bokeh_to_plot_index']=index
            dic['_bokeh_to_plot_dot_org']=self.dotData[y_menu[0]]
            dic['_bokeh_to_plot_line_org']=self.lineData[y_menu[0]]
            data=ColumnDataSource(data=dic)
            self.bokeh_fig.xaxis.axis_label=x_menu[0]
            self.bokeh_fig.yaxis.axis_label=y_menu[0]
            l1=Line(x='_bokeh_to_plot_x',y='_bokeh_to_plot_line',line_color='red',line_width=2)
            l2=Circle(x='_bokeh_to_plot_x',y='_bokeh_to_plot_dot',fill_color='blue',fill_alpha=0.4,size=7)
            r1=self.bokeh_fig.add_glyph(data,l1,name='line')
            r2=self.bokeh_fig.add_glyph(data,l2,name='dot')
            legend1 = Legend(items=[("predict",[self.bokeh_fig.renderers[0]]),("real",[self.bokeh_fig.renderers[1]])], location='top_right',click_policy='hide')
            self.bokeh_fig.add_layout(legend1)

            self.bokeh_fig.add_tools(
                HoverTool(tooltips = [('X,Y_true', '@_bokeh_to_plot_x,@_bokeh_to_plot_dot')],names=['dot'])
            )
            self.bokeh_fig.add_tools(
                HoverTool(tooltips = [('X,Y_predict', '@_bokeh_to_plot_x,@_bokeh_to_plot_line')],names=['line'])
            )
            callbackX = CustomJS(args=dict(source=data,axis=self.bokeh_fig.xaxis[0]), code="""
                    var data = source.data;
                    var f = cb_obj.value
                    let x=data['x_'+f]
                    let newList=[]
                    for(var i=0;i<x.length;i++){
                        newList.push({
                        value1: x[i],
                        value2: i
                        })
                    }
                    newList.sort(function(a,b) {
                        return ((a.value1 - b.value1))
                    })
                    for(var i=0;i<newList.length;i++){
                        data['_bokeh_to_plot_x'][i]=newList[i].value1
                        data['_bokeh_to_plot_index'][i]=newList[i].value2
                        data['_bokeh_to_plot_line'][i]=data['_bokeh_to_plot_line_org'][newList[i].value2]
                        data['_bokeh_to_plot_dot'][i]=data['_bokeh_to_plot_dot_org'][newList[i].value2]
                    }
                    axis.axis_label=f
                    source.change.emit();
                """)
            callbackY = CustomJS(args=dict(source=data,axis=self.bokeh_fig.yaxis[0]), code="""
                    var data = source.data;
                    var f = cb_obj.value
                    data['_bokeh_to_plot_dot_org']=data['dot_'+f]
                    data['_bokeh_to_plot_line_org']=data['line_'+f]
                    for(var i=0;i<data['_bokeh_to_plot_dot_org'].length;i++){
                        data['_bokeh_to_plot_dot'][i]=data['dot_'+f][data['_bokeh_to_plot_index'][i]]
                        data['_bokeh_to_plot_line'][i]=data['line_'+f][data['_bokeh_to_plot_index'][i]]
                    }
                    axis.axis_label=f
                    source.change.emit();
                """)

            #dp1 = Dropdown(label="X value",menu=x_menu,default_value=x_menu[0])
            dp1=Select(title="X-coordinate:",value=x_menu[0],options=x_menu)
            dp1.js_on_change('value', callbackX)
            #dp2 = Dropdown(label="Y value",menu=y_menu,default_value=y_menu[0])
            dp2=Select(title="Y-coordinate:",value=y_menu[0],options=y_menu)
            dp2.js_on_change('value', callbackY)
            self.bokeh_fig = column(row(dp1,dp2), self.bokeh_fig)
        except Exception as e:
            raise Exception(f'[{self.algoInfo["algoname"]}][do_bokeh_viz]{e}')
        
