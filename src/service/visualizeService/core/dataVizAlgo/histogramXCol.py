from service.visualizeService.core.dataVizAlgo.histogramX import histogramX

class histogramXCol(histogramX):
    def __init__(self,data,figName):
        self.algoInfo={}
        self.algoInfo['lib']='bokeh'
        self.algoInfo['friendlyname']=figName
        self.algoInfo['algoName']='histogramXCol'
        self.data={}
        self.data['x']=data
        self.bokeh_fig=self.init_figure(w=300,h=200)
        self.component=None
        
