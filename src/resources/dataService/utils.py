from params import params
import os
import csv
import pandas as pd
import glob
import zipfile
import uuid
import shutil
import logging
import numpy as np

class fileUidGenerator():
    def __init__(self):
        self.uid=str(uuid.uuid1())
        param=params()
        while len(glob.glob((param.filepath+"/"+self.uid+"*")))!=0:
            self.uid=str(uuid.uuid1())

class fileChecker():
    def __init__(self,filepath,projectType):
        self.filepath=filepath
        self.filetype=filepath[filepath.rfind("."):]
        self.projectType=projectType
        self.param=params()

    def check(self):
        if self.projectType=='cv':
            if  self.filetype=='.zip':
                return self.cvZipChecker()
        if self.projectType=='nlp':
            if self.filetype=='.tsv':
                return self.nlpTsvChecker()
        if self.projectType=='num':
            if self.filetype=='.csv':
                return self.numCsvChecker()

    def numCsvChecker(self):
        try:
            data=pd.read_csv(self.filepath)

            # check numerical value
            cols=data.columns.tolist()
            for c in cols:
                if data[c].dtype!=np.float64 and data[c].dtype!=np.int64:
                    os.remove(self.filepath)
                    return {"status":"error","msg":"csv should only contain numerical value: (Col "+c+")","data":{}}
                        
        except Exception as e:
            os.remove(self.filepath)
            return {"status":"error","msg":str(e),"data":{}}
        return {"status":"success","msg":"","data":{}}

    def cvZipChecker(self):

        folder=self.filepath[:self.filepath.rfind(".")]

        # unzipping
        try:
            with zipfile.ZipFile(self.filepath, 'r') as zip_ref:
                zip_ref.extractall(folder)
        except Exception as e:
            os.remove(self.filepath)
            return {"status":"error","msg":"unzip error","data":{}}
        
        #check #.csv and location
        csvFiles=glob.glob((folder+"/*.csv"))
        if len(csvFiles)!=1 or len(csvFiles)==0:
            os.remove(self.filepath)
            shutil.rmtree(folder)
            return {"status":"error","msg":"zip should contains only 1 csv file and be placed in the top path","data":{}}
        csvFile=csvFiles[0]
        csvFile=csvFile.replace("\\","/")
        try:
            data=pd.read_csv(csvFile)
        except Exception as e:
            return {"status":"error","msg":"error when parsing csv using panda. "+str(e),"data":{}}
        return {"status":"success","msg":"",'data':{}}
        
    def nlpTsvChecker(self):
        try:
            data=pd.read_csv(self.filepath, sep='\t')
        except Exception as e:
            return {"status":"error","msg":"error when parsing tsv using panda. "+str(e),"data":{}}
        return {"status":"success","msg":"",'data':{}}

    # def numericalCsvChecker_old():
    #     try:
    #         data=pd.read_csv(self.filepath)

    #         # check numerical value
    #         for v in data.values:
    #             for vv in v:
    #                 try:
    #                     tmp=float(vv)
    #                 except Exception as e:
    #                     os.remove(self.filepath)
    #                     return {"status":"error","msg":"csv should only contain numerical value: "+str(vv),"data":{}}
    #     except Exception as e:
    #         os.remove(self.filepath)
    #         return {"status":"error","msg":str(e),"data":{}}
    #     return {"status":"success","msg":"","data":{}}

    # def nlpTsvChecker_old():
    #     try:
    #         with open(self.filepath,newline='') as file:
    #             rows =[r for r in csv.reader(file, delimiter='\t')]
    #             cols=rows[0]

    #         # check num of value col
    #         if cols.count('value')!=1:
    #             os.remove(self.filepath)
    #             return {"status":"error","msg":"There should be (only) 1 col named value in csv file","data":{}}
            
    #         # check num of sentence col
    #         sentenceCol=cols.remove('value')
    #         if len(sentenceCol)==0:
    #             os.remove(self.filepath)
    #             return {"status":"error","msg":"There should be at least 1 col in csv that logs sentence","data":{}}

    #         # check numerical value
    #         data=pd.read_csv(self.filepath, sep='\t', header=0)
    #         for v in data['value'].values:
    #             try:
    #                 tmp=float(v)
    #             except Exception as e:
    #                 os.remove(self.filepath)
    #                 return {"status":"error","msg":"value col should only contain numerical value","data":{}}
       
    #     except Exception as e:
    #         os.remove(self.filepath)
    #         return {"status":"error","msg":str(e),"data":{}}
    #     return {"status":"success","msg":"","data":{}}

    # def cvZipChecker_old():
    #     import zipfile
    #     folder=self.filepath[:self.filepath.rfind(".")]
    #     '''
    #     @ try unzipping
    #     '''
    #     try:
    #         with zipfile.ZipFile(self.filepath, 'r') as zip_ref:
    #             zip_ref.extractall(folder)
    #     except Exception as e:
    #         os.remove(self.filepath)
    #         return {"status":"error","msg":"unzip error","data":{}}
        
    #     '''
    #     @ check #csv and location
    #     '''
    #     csvFiles=glob.glob(r(folder+"/*.csv"))
    #     if len(csvFiles)!=1 or len(csvFiles)==0:
    #         os.remove(self.filepath)
    #         shutil.rmtree(folder)
    #         return {"status":"error","msg":"zip should contains only 1 csv file","data":{}}
    #     if csvFiles[0].count("/")!=3:
    #         os.remove(self.filepath)
    #         shutil.rmtree(folder)
    #         return {"status":"error","msg":"csv file should be placed in the top path","data":{}}
    #     csvFile=csvFiles[0]

    #     '''
    #     @ check csv content and all img file
    #     '''
    #     try:
            
    #         with open(csvFile,newline='') as file:
    #             rows =[r for r in csv.reader(file)]
    #             cols=rows[0]

    #         # check num of value col
    #         if cols.count('value')!=1:
    #             os.remove(self.filepath)
    #             shutil.rmtree(folder)
    #             return {"status":"error","msg":"There should be (only) 1 col named value in csv file","data":{}}
            
    #         # check num of image col
    #         imageCol=cols.remove('value')
    #         if len(imageCol)==0:
    #             os.remove(self.filepath)
    #             shutil.rmtree(folder)
    #             return {"status":"error","msg":"There should be at least 1 col in csv that logs filename","data":{}}

    #         # check numerical value
    #         data=pd.read_csv(csvFile)
    #         for v in data['value'].values:
    #             try:
    #                 tmp=float(v)
    #             except Exception as e:
    #                 os.remove(self.filepath)
    #                 shutil.rmtree(folder)
    #                 return {"status":"error","msg":"value col should only contain numerical value","data":{}}
            
    #         # check image file existence
    #         for c in imageCol:
    #             for v in data[c].values:
    #                 if not os.path.exists(os.path.join(folder,v)):
    #                     os.remove(self.filepath)
    #                     shutil.rmtree(folder)
    #                     return {"status":"error","msg":"image file missing: "+v,"data":{}}
            
    #     except Exception as e:
    #         os.remove(self.filepath)
    #         shutil.rmtree(folder)
    #         return {"status":"error","msg":str(e),"data":{}}

    #     return {"status":"success","msg":"","data":{}}

def dTypeConverter(dtype):
    if dtype==np.float64:
        return "float"
    elif dtype==np.int64:
        return "int"
    else:
        return "str"

class getColType():
    def __init__(self,filepath,dataType):
        self.filepath=filepath
        self.dataType=dataType
    def get(self):
        if self.dataType=='num':
            try:
                data=pd.read_csv(self.filepath)
                logging.debug(f'[getColType] filepath:{self.filepath}')
                colNames=data.columns.tolist()
                j=[{"name":c,"type":dTypeConverter(data[c].dtype)} for c in colNames]
                logging.debug(f'[getColType]{j}')
            except Exception as e:
                return {"status":"error","msg":str(e),'data':{}}
            return {"status":"success","msg":"",'data':{"cols":j}}

        if self.dataType=='cv':
            try:
                csvFile=glob.glob(self.filepath+"/*.csv")[0]
                logging.debug(f'[getColType] filepath:{csvFile}')
                data=pd.read_csv(csvFile)
                colNames=data.columns.tolist()
                j=[{"name":c,"type":dTypeConverter(data[c].dtype)} for c in colNames]
                logging.debug(f'[getColType]{j}')
            except Exception as e:
                return {"status":"error","msg":str(e),'data':{}}
            return {"status":"success","msg":"",'data':{"cols":j}}
        if self.dataType=='nlp':
            try:
                data=pd.read_csv(self.filepath,sep='\t')
                logging.debug(f'[getColType] filepath:{self.filepath}')
                colNames=data.columns.tolist()
                j=[{"name":c,"type":dTypeConverter(data[c].dtype)} for c in colNames]
                logging.debug(f'[getColType]{j}')
            except Exception as e:
                return {"status":"error","msg":str(e),'data':{}}
            return {"status":"success","msg":"",'data':{"cols":j}}
