from params import params
import os
import csv
import pandas as pd

class fileChecker():
    def __init__(filepath):
        self.filepath=filepath
        self.filetype=filepath[filepath.rfind("."):]
        self.param=params()
        if self.filetype=='.csv':
            return self.numericalCsvChecker()
        if self.filetype=='.tsv':
            return self.nlpTsvChecker()
        if self.filetype=='.zip':
            return self.cvZipChecker()

    def numericalCsvChecker():
        try:
            data=pd.read_csv(self.filepath)

            # check numerical value
            for v in data.values:
                for vv in v:
                    try:
                        tmp=float(vv)
                    except Exception as e:
                        os.remove(self.filepath)
                        return {"status":"error","msg":"csv should only contain numerical value: "+str(vv),"data":{}}
        except Exception as e:
            os.remove(self.filepath)
            return {"status":"error","msg":str(e),"data":{}}
        return {"status":"success","msg":"","data":{}}

    def nlpTsvChecker():
        try:
            with open(self.filepath,newline='') as file:
                rows =[r for r in csv.reader(file, delimiter='\t')]
                cols=rows[0]

            # check num of value col
            if cols.count('value')!=1:
                os.remove(self.filepath)
                return {"status":"error","msg":"There should be (only) 1 col named value in csv file","data":{}}
            
            # check num of sentence col
            sentenceCol=cols.remove('value')
            if len(sentenceCol)==0:
                os.remove(self.filepath)
                return {"status":"error","msg":"There should be at least 1 col in csv that logs sentence","data":{}}

            # check numerical value
            data=pd.read_csv(self.filepath, sep='\t', header=0)
            for v in data['value'].values:
                try:
                    tmp=float(v)
                except Exception as e:
                    os.remove(self.filepath)
                    return {"status":"error","msg":"value col should only contain numerical value","data":{}}
       
        except Exception as e:
            os.remove(self.filepath)
            return {"status":"error","msg":str(e),"data":{}}
        return {"status":"success","msg":"","data":{}}

    def cvZipChecker():
        import zipfile
        folder=self.filepath[:self.filepath.rfind(".")]
        '''
        @ try unzipping
        '''
        try:
            with zipfile.ZipFile(self.filepath, 'r') as zip_ref:
                zip_ref.extractall(folder)
        except Exception as e:
            os.remove(self.filepath)
            return {"status":"error","msg":"unzip error","data":{}}
        
        '''
        @ check #csv and location
        '''
        csvFiles=glob.glob(r(folder+"/*.csv"))
        if len(csvFiles)!=1 or len(csvFiles)==0:
            os.remove(self.filepath)
            os.rmdir(folder)
            return {"status":"error","msg":"zip should contains only 1 csv file","data":{}}
        if csvFiles[0].count("/")!=3:
            os.remove(self.filepath)
            os.rmdir(folder)
            return {"status":"error","msg":"csv file should be placed in the top path","data":{}}
        csvFile=csvFiles[0]

        '''
        @ check csv content and all img file
        '''
        try:
            
            with open(csvFile,newline='') as file:
                rows =[r for r in csv.reader(file)]
                cols=rows[0]

            # check num of value col
            if cols.count('value')!=1:
                os.remove(self.filepath)
                os.rmdir(folder)
                return {"status":"error","msg":"There should be (only) 1 col named value in csv file","data":{}}
            
            # check num of image col
            imageCol=cols.remove('value')
            if len(imageCol)==0:
                os.remove(self.filepath)
                os.rmdir(folder)
                return {"status":"error","msg":"There should be at least 1 col in csv that logs filename","data":{}}

            # check numerical value
            data=pd.read_csv(csvFile)
            for v in data['value'].values:
                try:
                    tmp=float(v)
                except Exception as e:
                    os.remove(self.filepath)
                    os.rmdir(folder)
                    return {"status":"error","msg":"value col should only contain numerical value","data":{}}
            
            # check image file existence
            for c in imageCol:
                for v in data[c].values:
                    if not os.path.exists(os.path.join(folder,v)):
                        os.remove(self.filepath)
                        os.rmdir(folder)
                        return {"status":"error","msg":"image file missing: "+v,"data":{}}
            
        except Exception as e:
            os.remove(self.filepath)
            os.rmdir(folder)
            return {"status":"error","msg":str(e),"data":{}}

        return {"status":"success","msg":"","data":{}}