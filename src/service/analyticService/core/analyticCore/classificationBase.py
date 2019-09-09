from service.analyticService.core.analyticCore.analyticBase import analytic
import numpy as np
import pandas as pd
from service.visualizeService.core.analyticVizAlgo.heatmap import heatmap
from service.analyticService.core.analyticCore.evaluationTools import crossEntropy,classificationReport,confusionMatrix
from sklearn.metrics import confusion_matrix

class classification(analytic):
    def __init__(self, algoInfo, fid, action='train', mid=None):
        super().__init__(algoInfo, fid, action, mid)
    
    def test(self):
        self.txtRes = ""
        for k, v in self.outputDict.items():
            self.txtRes += f"{v}:\n"
            self.txtRes += f"  Cross Entropy: {crossEntropy(self.outputData[k],self.result[k])}\n"
            real=[self.c2d[v][str(i)] for i in  np.argmax(self.outputData[k],axis=1)]
            predicted=[self.c2d[v][str(i)] for i in  np.argmax(self.result[k],axis=1)]
            label=[k for k in self.d2c]
            self.txtRes += f"  Report:\n{classificationReport(real,predicted,label=label)}"
        self.visualize()
        return {"text": self.txtRes, "fig": self.vizRes}

    def projectVisualize(self):
        figs={}
        for k,v in self.outputDict.items():
            real=[self.c2d[v][str(i)] for i in  np.argmax(self.outputData[k],axis=1)]
            predicted=[self.c2d[v][str(i)] for i in  np.argmax(self.result[k],axis=1)]
            label=[k for k in self.d2c]
            cmx=confusion_matrix(real,predicted,labels=label)
            cmx=cmx.astype('float')/cmx.sum(axis=1)[:,np.newaxis]
            df=pd.DataFrame(cmx,columns=label)
            algo=heatmap(df,f"confusion matrix of {v}",color='blue',xName='predict',yName='real')
            algo.doBokehViz()
            algo.getComp()
            figs[f"confusion matrix of {v}"]=algo.component
        return figs
             
        

            