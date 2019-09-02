import pandas as pd
import numpy as np
from service.dataService.utils import getFileInfo,getColType,categoricalConverter,getDf
from service.analyticService.utils import modelUidGenerator
from params import params
import threading
import traceback

class analytic():
    def __init__(self,algoInfo,fid,par):
        self.algoName=algoInfo['algoname']
        self.fid=fid
        self.thread=None
        self.mid=modelUidGenerator().uid
        self.param=par
        self.sysparam=params()
        self.model=None
        self.dataDf=None
        self.dataDict=None
        self.result=None
        self.vizRes=None
        self.txtRes=None
        #read file info
        #get dataframe
        #build data dict
    
    def _getParams(self):
        #check param matching
        pass

    def _getData(self):
        #check colType matching
        pass

    def _saveModel(self):
        '''
        implement in project
        save model,param,dataCol,categoricalMapping to ./model/mid/
        '''
        raise NotImplementedError(f"{self.algoName} saveModel Not implemented")

    def _trainAlgo(self):
        '''
        implement in algo
        '''
        raise NotImplementedError(f"{self.algoName} Train algo Not implemented")
    
    def _trainWrapper(self):
        self._trainAlgo()
        self._saveModel()

    def train(self):
        # check params
        # check colType
        try:
            self.thread=threading.Thread(targert=self._trainWrapper)
            self.thread.start()
            self.thread.name=str(self.mid)
        except Exception as e:
            raise Exception(f"[{self.algoName}] {traceback.format_exc()}")

    def _predictAlgo(self):
        '''
        implement in algo
        use self.dataDf and self.dataDict to predict
        save the result as a 2D np.array in self.result
        '''
        pass
    
    def predict(self):
        '''
        implement in project
        call _predictAlgo
        merge self.dataDf and self.result
        write out newDf
        return fid
        '''
        pass
    
    def test(self):
        '''
        implement in project
        call _predictAlgo
        call visualize
        gengerate text to self.txtRes
        '''
        pass

    def _buidinVisualize(self):
        '''
        implement in project
        return [{div,script},{div,script},{div,script}]
        '''
        pass
    
    def _visualizeAlgo(self):
        '''
        implement in algo if needed
        return [{div,script},{div,script},{div,script}]
        '''
        return []

    def visualize(self):
        vizRes=self._buidinVisualize()
        vizRes.extend(self._visualizeAlgo())
        self.vizRes=vizRes
