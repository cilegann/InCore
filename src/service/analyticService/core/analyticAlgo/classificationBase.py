from service.analyticService.core.analyticAlgo.analyticBase import analytic
import numpy as np
from service.visualizeService.core.analyticVizAlgo.dotLine import dotLine
from service.analyticService.core.analyticAlgo.evaluationTools import crossEntropy,classificationReport,confusionMatrix

class regression(analytic):
    def __init__(self, algoInfo, fid, action='train', mid=None):
        super().__init__(algoInfo, fid, action, mid)
    
    def test(self):
        self.txtRes = ""
        for k, v in self.outputData.items():
            self.txtRes += f"{k}:\n"
            self.txtRes += f"  Cross Entropy: {crossEntropy(self.result[k],v)}\n"
            self.txtRes += f"  Report:\n{classificationReport(np.argmax(self.result[k],axis=1),np.argmax(v,axis=1))}"
        self.visualize()
        return {"text": self.txtRes, "fig": self.vizRes}

    def projectVisualize(self):
        for k,v in self.outputData.items():
            

            
        allInputCols = {}
        allRealCols = {}
        allPredictCols = {}
        figs = {}
        for k, v in self.inputDict.items():
            for col in v:
                if self.colType[col] == 'float' or self.colType[col] == 'int':
                    allInputCols[col] = self.dataDf[col]
        for k, v in self.outputDict.items():
            if self.colType[v] == 'float' or self.colType[v] == 'int':
                allRealCols[v] = self.dataDf[v]
                allPredictCols[v] = self.result[k]
        for ink, inv in allInputCols.items():
            for outk, outv in allRealCols.items():
                tmpData = {"x": inv, "y_dot": outv, "y_line": allPredictCols[outk]}
                tmpColName={"x":ink,"y":outk}
                figName=f"{ink}-{outk}"
                algo=dotLine(tmpData,tmpColName,figName)
                algo.doBokehViz()
                algo.getComp()
                figs[figName]=algo.component
        return figs
             
        

            