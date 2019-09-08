from service.analyticService.core.correlationCore.correlationBase import correlation

class pearson(correlation):
    def __init__(self,fid):
        super().__init__(fid,"pearson","Pearson correlation coefficient")
    def calculate(self):
        self.corr=self.df.corr(method='pearson')