from service.analyticService.core.correlationCore.correlationBase import correlation

class spearman(correlation):
    def __init__(self,fid):
        super().__init__(fid,"spearman","Spearman correlation coefficient")
    def calculate(self):
        self.corr=self.df.corr(method='spearman')