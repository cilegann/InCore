from service.visualizeService.core.dataVizAlgo.histogramX import histogramX

class histogramXCol(histogramX):
    def __init__(self,data,figName):
        try:
            self.algoInfo={}
            self.algoInfo['lib']='bokeh'
            self.algoInfo['friendlyname']=figName
            self.algoInfo['algoname']='histogramXCol'
            self.data={}
            self.data['x']=data
            self.bokeh_fig=self.init_figure(w=300,h=200)
            self.component=None
        except Exception as e:
            raise Exception(f'[analyticViz][{self.algoInfo["algoname"]}]{e}')
        
