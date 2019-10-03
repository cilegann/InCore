class params():
    def __init__(self):
        self.host='140.112.26.132'
        self.port=8003
        self.secretkey='iloveraid1'
        self.filepath='./db'
        self.modelpath='./models'
        self.imgpath='./images'
        self.servicepath='./src/service/'

        self.dataCollectServiceRoot=self.servicepath+'dataService/'
        self.visualizeServiceRoot=self.servicepath+'visualizeService/'
        self.analyticServiceRoot=self.servicepath+'analyticService/'

        self.dataVizAlgoReg=self.visualizeServiceRoot+'core/dataVizReg.json'
        self.dataPreprocessAlgoReg=self.analyticServiceRoot+'core/preprocessCore/preprocessReg.json'
        self.correlationAlgoReg=self.analyticServiceRoot+'core/correlationCore/correlationReg.json'
        self.analyticAlgoReg=self.analyticServiceRoot+'core/analyticCore/analyticReg.json'

        self.dataExtensionType={'num':['.csv'],'cv':['.zip'],'nlp':['.tsv']}
        #self.dataExtensionType={'num':['.csv']}
        self.dataProjectType={'num':['regression','classification','abnormal','clustering'],'cv':['regression','classification'],'nlp':['regression','classification']}
        #self.dataProjectType={'num':['regression']}
        self.dbhost='140.112.26.132'
        self.dbuser='ican'
        self.dbpwd='lab125a'
        self.dbschema='incore'

        self.classifiableThreshold=5