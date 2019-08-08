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
from utils import sql

def getFileInfo(fid):
    try:
        db=sql()
        db.cursor.execute(f"select * from files where `fid`='{fid}'")
        data=db.cursor.fetchall()
        data=[[tt for tt in t] for t in data]
        return {"status":"success","msg":"","data":data}
    except Exception as e:
        logging.error(f'[getFileInfo]{e}')
        return {"status":"error","msg":str(e),"data":{}}
    finally:
        db.conn.close()

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
        # check if parsable, if numerical
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
            logging.error(f'[fileChecker]{e}')
            return {"status":"error","msg":str(e),"data":{}}
        return {"status":"success","msg":"","data":{}}

    def cvZipChecker(self):
        # try unzippable, csv location, csv parsable
        folder=self.filepath[:self.filepath.rfind(".")]
        try:
            with zipfile.ZipFile(self.filepath, 'r') as zip_ref:
                zip_ref.extractall(folder)
        except Exception as e:
            os.remove(self.filepath)
            logging.error(f'[fileChecker]{e}')
            return {"status":"error","msg":"unzip error","data":{}}
        os.remove(self.filepath)

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
            logging.error(f'[fileChecker]{e}')
            return {"status":"error","msg":"error when parsing csv using panda. "+str(e),"data":{}}
        return {"status":"success","msg":"",'data':{}}
        
    def nlpTsvChecker(self):
        # try tsv parsable
        try:
            data=pd.read_csv(self.filepath, sep='\t')
        except Exception as e:
            logging.error(f'[fileChecker]{e}')
            return {"status":"error","msg":"error when parsing tsv using panda. "+str(e),"data":{}}
        return {"status":"success","msg":"",'data':{}}

def dTypeConverter(dtype):
    if dtype==np.float64:
        return "float"
    elif dtype==np.int64:
        return "int"
    else:
        return "string"

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
                j=[{"name":c,"type":dTypeConverter(data[c].dtype) } for c in colNames]
                logging.debug(f'[getColType]{j}')
            except Exception as e:
                logging.error(f'[getColType]{e}')
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
                logging.error(f'[getColType]{e}')
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
                logging.error(f'[getColType]{e}')
                return {"status":"error","msg":str(e),'data':{}}
            return {"status":"success","msg":"",'data':{"cols":j}}
