from service.analyticService.core.analyticCore.analyticBase import analytic
import numpy as np
import pandas as pd
from service.visualizeService.core.analyticVizAlgo.heatmap import heatmap
from service.analyticService.core.analyticCore.evaluateTools import crossEntropy,classificationReport
from sklearn.metrics import confusion_matrix
import importlib

class classification(analytic):
    def __init__(self, algoInfo, fid, action='train', mid=None):
        super().__init__(algoInfo, fid, action, mid)
        self.metric=list(set(self.metric) & set(["cross_entropy"])) 
    
    def test(self):
        if self.action=='test':
            self.clearSession()
        module=importlib.import_module(f"service.analyticService.core.analyticCore.evaluateTools")
        importlib.reload(module)
        for k, v in self.outputDict.items():
            self.txtRes += f"{v}:\n"
            for m in self.metric:
                attr=getattr(module,m)
                self.txtRes+=attr(self.outputData[k],seld.result[k])
            # self.txtRes += f"  Cross Entropy: {crossEntropy(self.outputData[k],self.result[k])}\n"
            real=[str(self.c2d[v][str(i)]) for i in  np.argmax(self.outputData[k],axis=1)]
            predicted=[str(self.c2d[v][str(i)]) for i in  np.argmax(self.result[k],axis=1)]
            label=[k for k in self.d2c[v]]
            self.formRes[f"Report-{v}"]=classificationReport(real,predicted,label=label)
            #self.txtRes += f"  Report:\n{classificationReport(real,predicted,label=label)}"
        self.visualize()
        return {"text": self.txtRes, "fig": self.vizRes,"form":self.formRes}

    def projectVisualize(self):
        figs={}
        for k,v in self.outputDict.items():
            real=[str(self.c2d[v][str(i)]) for i in  np.argmax(self.outputData[k],axis=1)]
            predicted=[str(self.c2d[v][str(i)]) for i in  np.argmax(self.result[k],axis=1)]
            label=[k for k in self.d2c[v]]
            cmx=confusion_matrix(real,predicted,labels=label)
            cmx=cmx.astype('float')/cmx.sum(axis=1)[:,np.newaxis]
            df=pd.DataFrame(cmx,columns=label)
            df = df.fillna(0)
            algo=heatmap(df,f"confusion matrix of {v}",color='blue',xName='predict',yName='real')
            algo.doBokehViz()
            algo.getComp()
            figs[f"confusion matrix of {v}"]=algo.component
        return figs
             
        

            