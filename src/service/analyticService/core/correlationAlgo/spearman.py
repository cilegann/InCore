from service.analyticService.core.correlation import correlation

class spearman(correlation):
    def __init__(self,fid):
        super().__init__(fid,"spearman")
    def calculate(self):
        self.corr=self.df.corr(method='spearman')