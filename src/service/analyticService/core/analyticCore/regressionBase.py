from service.analyticService.core.analyticCore.analyticBase import analytic
import numpy as np
from service.visualizeService.core.analyticVizAlgo.dotLineSelect import dotLineSelect
import importlib

class regression(analytic):
    def __init__(self, algoInfo, fid, action='train', mid=None):
        super().__init__(algoInfo, fid, action, mid)
        self.metric=list(set(self.metric) & set(["MAE","MSE","RMSE"])) 
    
    def test(self):
        if self.action=='test':
            self.clearSession()
        module=importlib.import_module(f"service.analyticService.core.analyticCore.evaluateTools")
        importlib.reload(module)
        for k, v in self.outputData.items():
            self.txtRes += f"{self.outputDict[k]}:\n"
            for m in self.metric:
                attr=getattr(module,m)
                self.txtRes += attr(v,self.result[k])
            # self.txtRes += f"  MAE: {(np.abs(v-self.result[k])).mean()}\n"
            # self.txtRes += f"  MSE: {((v-self.result[k])**2).mean()}\n"
            # self.txtRes += f"  RMSE: {np.sqrt(((v-self.result[k])**2).mean())}\n"
            self.txtRes += "\n"
        self.visualize()
        return {"text": self.txtRes, "fig": self.vizRes,"form":self.formRes}

    def projectVisualize(self):
        allInputCols = {}
        allRealCols = {}
        allPredictCols = {}
        figs = {}
        for k, v in self.inputDict.items():
            for col in v:
                if self.colType[col]['type'] == 'float' or self.colType[col]['type'] == 'int':
                    allInputCols[col] = self.dataDf[col]
        for k, v in self.outputDict.items():
            if self.colType[v]['type'] == 'float' or self.colType[v]['type'] == 'int':
                allRealCols[v] = self.dataDf[v]
                allPredictCols[v] = self.result[k]
        if len(allInputCols)==0:
            return {}
        else:
            algo=dotLineSelect(allInputCols,allRealCols,allPredictCols)
            algo.doBokehViz()
            algo.getComp()
            return {"regression result":algo.component}
        # for ink, inv in allInputCols.items():
        #     for outk, outv in allRealCols.items():
        #         tmpData = {"x": inv, "y_dot": outv, "y_line": allPredictCols[outk]}
        #         tmpColName={"x":ink,"y":outk}
        #         figName=f"{ink}-{outk}"
        #         algo=dotLine(tmpData,tmpColName,figName)
        #         algo.doBokehViz()
        #         algo.getComp()
        #         figs[figName]=algo.component
        # return figs
             
        

            