class params():
    def __init__(self):
        self.host='140.112.26.135'
        self.port=8787
        self.secretkey='iloveraid1'
        self.filepath='./db'
        self.modelpath='./models'
        self.imgpath='./images'
        self.servicepath='./src/service/'

        self.dataCollectServiceRoot=self.servicepath+'dataService/'
        self.visualizeServiceRoot=self.servicepath+'visualizeService/'
        self.analyticServiceRoot=self.servicepath+'analyticService/'

        self.dataVizAlgoReg=self.visualizeServiceRoot+'core/dataViz.json'

        self.dataPreprocessAlgoReg=self.analyticServiceRoot+'core/preprocessAlgo/preprocess.json'

        self.dataFileType={'num':['.csv'],'cv':['.zip'],'nlp':['.tsv']}
        self.dataProjectType={'num':['Regression','Classification','Abnormal','Clustering'],'cv':['Regression','Classification'],'nlp':['Regression','Classification']}
        self.dbhost='140.112.26.132'
        self.dbuser='ican'
        self.dbpwd='lab125a'
        self.dbschema='incore'