from params import params
from service.dataService.utils import getFileInfo,getDf,getColType,fileUidGenerator,dTypeConverter,classifiableChecker
from utils import sql
import logging
import json
import numpy as np
import pandas as pd
import importlib
import os
import shutil
import traceback

class preprocess():
    def __init__(self,fid,action):
        try:
            self.params=params()
            self.fid=fid
            self.action=action
            fid,self.dataType,self.path,self.numFile,status,actionFile=getFileInfo(self.fid)[0]
            self.colType=getColType(self.numFile,self.dataType).get()
            self.df=getDf(self.numFile,self.dataType).get()
            self.data={}
            for c in self.colType:
                self.data[c['name']]={'colType':c['type'],'classifiable':c['classifiable'],'do':False}
                # self.data={"col1":{"type":"int","action":action,"data":data}}
            for c in self.action:
                if c['col'] in self.data:
                    self.data[c['col']]['missingFiltering']=c['missingFiltering']
                    self.data[c['col']]['outlierFiltering']=c['outlierFiltering']
                    self.data[c['col']]['normalize']=c['normalize']
                    self.data[c['col']]['stringCleaning']=c['stringCleaning']
                    self.data[c['col']]['data']=np.asarray(self.df[c['col']])
                    self.data[c['col']]['do']=True
            okCount=0
            for k,v in self.data.items():
                if 'data' in v:
                    okCount+=1
                    break
            if okCount==0:
                raise Exception(f"[Preprocess Init] actionCol and fileCol not corresponed at all")
        except Exception as e:
            raise Exception(f"[Preprocess Init]{traceback.format_exc()}")

    def preview(self):
        try:
            for k,v in self.data.items():
                if v['do']:
                    previewData=v
            originDataLen=len(previewData['data'])
            originData=previewData['data']

            if previewData['missingFiltering']=='1':
                from service.analyticService.core.preprocessCore.missingFiltering import missingFiltering
                previewData['data']=previewData['data'][ missingFiltering().getRetainIndex([previewData['data']],[previewData['colType']],self.path) ]
                if previewData['colType']=='int':
                    previewData['data']=previewData['data'].astype(np.int64)

            if len(previewData['data'])!=0 and previewData['outlierFiltering']!='0' and previewData['colType']!='string' and previewData['colType']!='path':
                module=importlib.import_module(f"service.analyticService.core.preprocessCore.outlierFilteringAlgo.{previewData['outlierFiltering']}")
                algo=getattr(module,previewData['outlierFiltering'])
                previewData['data']=previewData['data'][algo(previewData['data']).getRetainIndex()]
            
            if len(previewData['data'])!=0 and previewData['normalize']!='0' and previewData['colType']!='string' and previewData['colType']!='path':
                module=importlib.import_module(f"service.analyticService.core.preprocessCore.normalizeAlgo.{previewData['normalize']}")
                algo=getattr(module,previewData['normalize'])
                previewData['data']=algo(previewData['data']).do()
            
            if len(previewData['data'])!=0 and "0" not in previewData['stringCleaning'] and previewData['colType']=='string':
                # act=json.loads(previewData['stringCleaning'])
                act=previewData['stringCleaning']
                for a in act:
                    module=importlib.import_module(f"service.analyticService.core.preprocessCore.stringCleaningAlgo.{a}")
                    algo=getattr(module,a)
                    previewData['data']=algo(previewData['data']).do()
            
            processedDataLen=len(previewData['data'])
            processedData=previewData['data']
            processedColType=dTypeConverter(processedData,self.dataType)
            processedClassifiable=classifiableChecker(processedData,processedColType)
            msg=f'Num of rows reduced {originDataLen-processedDataLen} from {originDataLen} to {processedDataLen}'
            beforeComp="None"
            afterComp="None"

            if previewData['classifiable']==1:
                from service.visualizeService.core.analyticVizAlgo.barCntCol import barCntCol as algo
            elif previewData['colType']=='float' or previewData['colType']=='int':
                from service.visualizeService.core.analyticVizAlgo.histogramXCol import histogramXCol as algo
            
            before=algo(originData,"Before")
            before.doBokehViz()
            before.getComp()
            beforeComp=before.component

            if processedClassifiable==1:
                from service.visualizeService.core.analyticVizAlgo.barCntCol import barCntCol as algo
            elif processedColType=='float' or processedColType=='int':
                from service.visualizeService.core.analyticVizAlgo.histogramXCol import histogramXCol as algo
            after=algo(processedData,"After")
            after.doBokehViz()
            after.getComp()
            afterComp=after.component
        
            return msg,beforeComp,afterComp
        except Exception as e:
            import traceback
            raise Exception(f"[Preprocess Preview]{traceback.format_exc()}")

        

    def do(self):
        try:
            dataLen=0
            #missing value filtering
            from service.analyticService.core.preprocessCore.missingFiltering import missingFiltering
            for k,v in self.data.items():
                dataLen=len(v['data'])
            if dataLen!=0:
                data=[]
                colType=[]
                for k,v in self.data.items():
                    if 'missingFiltering' in v and v['missingFiltering']=='1':
                        data.append(v['data'])
                        colType.append(v['colType'])
                retainIndex=missingFiltering().getRetainIndex(data,colType,self.path)
                for k,v in self.data.items():
                    self.data[k]['data']=v['data'][retainIndex]
                    if v['colType']=='int':
                        self.data[k]['data']=v['data'].astype(np.int64)
                    dataLen=len(self.data[k]['data'])

            # outlier filtering
            if dataLen!=0:
                retainIndex=np.asarray([True for i in range(dataLen)])
                for k,v in self.data.items():
                    if 'outlierFiltering' in v and v['outlierFiltering']!="0" and v['colType']!='string' and v['colType']!='path':
                        module=importlib.import_module(f"service.analyticService.core.preprocessCore.outlierFilteringAlgo.{v['outlierFiltering']}")
                        algo=getattr(module,v['outlierFiltering'])
                        ri=algo(v['data']).getRetainIndex()
                        retainIndex=np.logical_and(retainIndex,ri)
                for k,v in self.data.items():
                    self.data[k]['data']=v['data'][retainIndex]
                    dataLen=len(self.data[k]['data'])

            # normalize
            if dataLen!=0:
                for k,v in self.data.items():
                    if 'normalize' in v and v['normalize']!="0" and v['colType']!='string' and v['colType']!='path':
                        module=importlib.import_module(f"service.analyticService.core.preprocessCore.normalizeAlgo.{v['normalize']}")
                        algo=getattr(module,v['normalize'])
                        self.data[k]['data']=algo(v['data']).do()
            if dataLen!=0:
                for k,v in self.data.items():
                    if 'stringCleaning' in v and "0" not in v['stringCleaning'] and v['colType']=='string':
                        # act=json.loads(v['stringCleaning'])
                        act=v['stringCleaning']
                        for a in act:
                            module=importlib.import_module(f"service.analyticService.core.preprocessCore.stringCleaningAlgo.{a}")
                            algo=getattr(module,a)
                            self.data[k]['data']=algo(v['data']).do()

            uid=fileUidGenerator().uid
            logging.info(f"[Preprocess Do] New UID: {uid}")
            newdata={k:v['data'] for k,v in self.data.items()}
            colNames=self.df.columns.tolist()
            newDf=pd.DataFrame(newdata,columns=colNames)

            if self.dataType!='cv':
                fileType=self.numFile[self.numFile.rfind("."):]
                newNumFile=os.path.join(self.params.filepath,uid+fileType)
                newPath=newNumFile
                actionFile=os.path.join(self.params.filepath,uid+'.json')
                if fileType=='.tsv':
                    newDf.to_csv(newNumFile,sep='\t',index=False)
                if fileType=='.csv':
                    newDf.to_csv(newNumFile,index=False)
            else:
                oldNumFileName=self.numFile[self.numFile.rfind("/")+1:]
                numFileType=self.numFile[self.numFile.find("."):]
                newNumFile=os.path.join(self.params.filepath,uid,oldNumFileName)
                newPath=os.path.join(self.params.filepath,uid)
                actionFile=os.path.join(self.params.filepath,uid+'.json')
                shutil.copytree(self.path,newPath)
                newDf.to_csv(newNumFile,index=False)
            with open(actionFile,'w') as file:
                json.dump(self.action,file)
            newNumFile=newNumFile.replace("\\","/")
            newPath=newPath.replace("\\","/")
            actionFile=actionFile.replace("\\","/")
            try:
                db=sql()
                db.cursor.execute(f"insert into files (`fid`,`dataType`,`path`,`numFile`,`inuse`,`preprocessAction`) values ('{uid}','{self.dataType}','{newPath}','{newNumFile}',False,'{actionFile}');")
                db.conn.commit()
            except Exception as e:
                raise Exception(e)
            finally:
                db.conn.close()
            return uid

        except Exception as e:
            import traceback
            raise Exception(f"[Preprocess Do]{traceback.format_exc()}")