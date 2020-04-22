from service.analyticService.core.analyticCore.analyticBase import analytic
from params import params
from service.analyticService.utils import modelUidGenerator
from service.dataService.utils import getFileInfo,getColType,categoricalConverter,getDf,lockFile,fileUidGenerator
import json
import traceback
import os
import shutil
from utils import sql
from sklearn.metrics import confusion_matrix, silhouette_samples, silhouette_score
import numpy as np
import pandas as pd
from service.visualizeService.core.analyticVizAlgo.heatmap import heatmap
from service.visualizeService.core.analyticVizAlgo.clusteringDot import clusteringDot

'''
prediction result should be saved to self.result['cluster'] as a 1D np array
'''

class clustering(analytic):

    def __init__(self, algoInfo, fid, action='train', mid=None):
        super().__init__(algoInfo, fid, action, mid)
        self.metric=list(set(self.metric) & set(["Average silhouette score"])) 

    def predict(self):
        self.clearSession()
        self.dataDf['cluster']=self.result['cluster']
        uid=fileUidGenerator().uid
        if self.dataType=='cv':
            oldNumFileName=self.numFile[self.numFile.rfind("/")+1:]
            numFileType=self.numFile[self.numFile.find("."):]
            newNumFile=os.path.join(self.sysparam.filepath,uid,oldNumFileName)
            newPath=os.path.join(self.sysparam.filepath,uid)
            actionFile=os.path.join(self.sysparam.filepath,uid+'.json')
            shutil.copytree(self.path,newPath)
            self.dataDf.to_csv(newNumFile,index=False)
        else:
            fileType=self.numFile[self.numFile.rfind("."):]
            newNumFile=os.path.join(self.sysparam.filepath,uid+fileType)
            newPath=newNumFile
            if fileType=='.tsv':
                self.dataDf.to_csv(newNumFile,sep='\t',index=False)
            if fileType=='.csv':
                self.dataDf.to_csv(newNumFile,index=False)
        if self.preprocessActionFile:
            actionFile=os.path.join(self.sysparam.filepath,uid+'.json')
            shutil.copyfile(self.preprocessActionFile,actionFile)
        try:
            db=sql()
            newPath=newPath.replace("\\","/")
            newNumFile=newNumFile.replace("\\","/")
            if self.preprocessActionFile:
                actionFile=actionFile.replace("\\","/")
                db.cursor.execute(f"insert into files (`fid`,`dataType`,`path`,`numFile`,`inuse`,`preprocessAction`) values ('{uid}','{self.dataType}','{newPath}','{newNumFile}',False,'{actionFile}');")
            else:
                db.cursor.execute(f"insert into files (`fid`,`dataType`,`path`,`numFile`,`inuse`) values ('{uid}','{self.dataType}','{newPath}','{newNumFile}',False);")
            db.conn.commit()
        except Exception as e:
            raise Exception(e)
        finally:
            db.conn.close()
        return uid
    
    def test(self):
        if self.action=='test':
            self.clearSession()
        try:
            x=[]
            for k,v in self.inputDict.items():
                for col in v:
                    if self.colType[col]['type']=='float' or self.colType[col]['type']=='int':
                        x.append(self.dataDf[col])
            x=np.asarray(x)
            x=np.transpose(x)        
            silhouette_avg = silhouette_score(x, self.result['cluster'])
            self.txtRes+=f"Average silhouette score: {silhouette_avg}"
        except Exception as e:
            if self.txtRes=="":
                self.txtRes="Average silhouette score: Nan"
        try:
            self.visualize()
        except:
            pass
        return {"text": self.txtRes, "fig": self.vizRes,"form":self.formRes}

    def projectVisualize(self):
        figs={}
        allInput={}
        for k,v in self.inputDict.items():
            for col in v:
                if self.colType[col]['type']=='float' or self.colType[col]['type']=='int':
                    allInput[col]=self.dataDf[col]
        algo=clusteringDot(allInput,self.result["cluster"],"preview")
        algo.doBokehViz()
        algo.getComp()
        figs["Preview"]=algo.component
        return figs
    