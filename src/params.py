from configparser import ConfigParser, SafeConfigParser
import os
from datetime import datetime, time

class params():
    def __init__(self):
        cfg=SafeConfigParser(os.environ)
        cfg.read('secret.cfg')
        self.host=cfg.get('DEFAULT','host')
        self.port=int(cfg.get('DEFAULT','port'))
        self.secretkey=cfg.get('DEFAULT','secretkey')
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
        self.dbhost=cfg.get('DEFAULT','dbhost')
        self.dbuser=cfg.get('DEFAULT','dbuser')
        self.dbpwd=cfg.get('DEFAULT','dbpwd')
        self.dbschema=cfg.get('DEFAULT','dbschema')

        self.classifiableThreshold=22

        statusCfg=SafeConfigParser(os.environ)
        statusCfg.read('serverStatus.cfg')

        self.maintainBegin=time(23,00)
        self.maintainEnd=time(1,00)
        self.maintaining=statusCfg.getboolean('DEFAULT','maintaining')
        self.maintainMsg="為了提供穩定訓練環境，現在為系統維護時段，您仍可正常使用<br>但可能會出現瞬斷、模型訓練中止等情況。抱歉造成不便"

        self.analyticModuleUploadDeadline=datetime.strptime(statusCfg.get("DEFAULT","analyticModuleUploadDeadline"),'%Y-%m-%d %H:%M')
        self.analyticModuleUploadOnline=statusCfg.getboolean('DEFAULT','analyticModuleUploadOnline')