from service.visualizeService.core.dataVizBase import dataViz
from bokeh.models import HoverTool,ColumnDataSource
from bokeh.palettes import Category20,Category10
from random import shuffle
import pandas as pd
import logging
import numpy as np
from sklearn.decomposition import PCA
from service.analyticService.core.preprocessCore.missingFiltering import missingFiltering

class scatterPCAClass(dataViz):
    def __init__(self,algoInfo,dataCol,fid):
        super().__init__(algoInfo,dataCol,fid)

    def doBokehViz(self):
        try:
            rawdata=self.data['all']
            c=self.data['value']
            if max(c)>9:
                cmap=Category20[20]
            else:
                cmap=Category10[10]
            # shuffle(cmap)

            data=[]
            for col in rawdata.columns.tolist():
                if col!=self.dataCol['value']:
                    tmp=np.asarray(rawdata[col])
                    if tmp.dtype==np.int64 or tmp.dtype==np.float64:
                        data.append(tmp)
            data.append(c)
            types=['float' for i in range(len(data)-1)]+[self.colTypes[self.dataCol['value']]]
            filted=missingFiltering().filtCols(data,types,[True for i in range(len(data))])
            data=filted[:-1]
            c=filted[-1]
            if len(set(c))>9:
                cmap=Category20[20]
            else:
                cmap=Category10[10]
            cateMapping={str(k):i for i,k in enumerate(list(set(c)))}
            color=[cmap[cateMapping[str(k)]] for k in c]
            data=np.asarray(data)
            if len(data)>2:
                data=np.transpose(data)
                pca=PCA(n_components=2)
                pcaed=np.transpose(pca.fit_transform(data))
                source=ColumnDataSource(pd.DataFrame({'x':pcaed[0],'y':pcaed[1],'class':c,'color':color}))
            elif len(data)==2:
                source=ColumnDataSource(pd.DataFrame({'x':data[0],'y':data[1],'class':c,'color':color}))
            else:
                raise Exception(f'[{self.algoInfo["algoname"]}][do_bokeh_viz] num of column must greater than 2')
            self.bokeh_fig.add_tools(
                HoverTool(
                    show_arrow=True, 
                    line_policy='next',
                    tooltips=[
                        ('X_value', '$data_x'),
                        ('Y_value', '$data_y'),
                        ('class','@class')
                    ]
                )
            )
            self.bokeh_fig.scatter('x','y',source=source, color='color' , size=5,legend='class')
        except Exception as e:
            raise Exception(f'[{self.algoInfo["algoname"]}][do_bokeh_viz] {e}')
