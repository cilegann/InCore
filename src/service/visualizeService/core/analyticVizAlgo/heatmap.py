from service.visualizeService.core.dataVizBase import dataViz
from bokeh.plotting import figure
from bokeh.models import LinearColorMapper, HoverTool
from bokeh.transform import transform

class heatmap(dataViz):
    def __init__(self,dataFrame,figName,absColor=True,color='red',w=625,h=400,fontSize=18,minValue=None,maxValue=None,xName="",yName=""):
        try:
            self.algoInfo={}
            self.algoInfo['lib']='bokeh'
            self.algoInfo['friendlyname']=figName
            self.algoInfo['algoname']='heatmap'
            self.data=dataFrame
            self.w=w
            self.h=h
            self.xName=xName
            self.yName=yName
            self.bokeh_fig=self.init_figure()
            self.absColor=absColor
            self.color=color
            self.fontSize=fontSize
            self.minValue=minValue
            self.maxValue=maxValue
            
            self.component=None
        except Exception as e:
            raise Exception(f'[analyticViz][{self.algoInfo["algoname"]}]{e}')

    def init_figure(self):
        try:
            p=figure(title = self.algoInfo['friendlyname'], sizing_mode="fixed", plot_width=self.w, plot_height=self.h,tools='pan,wheel_zoom,box_zoom,save,reset',x_range=list(self.data.columns),y_range=list(reversed(self.data.columns)))
            p.toolbar.logo=None
            p.xaxis.axis_label=self.xName
            import math
            if max([len(d) for d in self.data.columns])>10:
                p.xaxis.major_label_orientation=math.pi/4
                p.yaxis.major_label_orientation=math.pi/4
            p.yaxis.axis_label=self.yName
            return p
        except Exception as e:
            raise Exception(f'[init_figure]{e}')

    def doBokehViz(self):
        try:
            from itertools import chain
            value=list(chain.from_iterable([x for x in list(self.data.apply(tuple))]))
            text=[round(x,2) for x in value]
            if self.absColor:
                absValue=[abs(number) for number in value]
            else:
                absValue=value
            source={
                'x':[i for i in list(self.data.columns) for j in list(self.data.columns)],
                'y': list(self.data.columns)*len(self.data.columns),
                'value':value,
                'abs':absValue,
                'text':text
            }
            from bokeh.palettes import inferno,YlOrRd,Magma,PuBu,Greys
            if self.color=='red':
                blockColor=YlOrRd[9]
                blockColor.reverse()
                textColor=[Magma[3][0],Magma[3][2]]
            elif self.color=='blue':
                blockColor=PuBu[9]
                blockColor.reverse()
                textColor=[Greys[5][0],Greys[5][4]]
            if not self.minValue:
                self.minValue=min(absValue)
            if not self.maxValue:
                self.maxValue=max(absValue)
            blockMapper=LinearColorMapper(palette=blockColor, low=self.minValue, high=self.maxValue)
            textMapper=LinearColorMapper(palette=textColor, low=self.minValue, high=self.maxValue)
            self.bokeh_fig.rect(x="x", y="y", width=1, height=1, source=source,line_color=None, fill_color=transform('abs', blockMapper))
            if max([len(d) for d in self.data.columns]) > 10 or len(self.data.columns)>8:
                self.fontSize=10
            if max([len(d) for d in self.data.columns]) > 15 or len(self.data.columns)>12:
                self.fontSize=8
            if max([len(d) for d in self.data.columns]) > 15 or len(self.data.columns)>15:
                self.fontSize=6
            self.bokeh_fig.text(x="x", y="y",text='text', source=source,text_font_size=f'{self.fontSize}pt',text_font_style='bold',text_align='center',text_baseline='middle',text_color=transform('abs',textMapper))
            self.bokeh_fig.add_tools(
                HoverTool(tooltips = [("Column", "@x , @y"),('Value', '@value'),])
            )
        except Exception as e:
            raise Exception(f'[{self.algoInfo["algoname"]}][doBokehViz]{e}')