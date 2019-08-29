from service.visualizeService.core.dataVizAlgo.barCnt import barCnt

class barCntCol(barCnt):
    def __init__(self,data,figName):
        self.algoInfo={}
        self.algoInfo['lib']='bokeh'
        self.algoInfo['friendlyname']=figName
        self.algoInfo['algoName']='barCntCol'
        self.data={}
        self.data['x']=data
        self.bokeh_fig=self.init_figure(w=300,h=200)
        self.component=None
        
