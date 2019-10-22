import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_fscore_support as score
from texttable import Texttable
import json

def crossEntropy( targets,predictions, epsilon=1e-12):
    predictions = np.clip(predictions, epsilon, 1. - epsilon)
    N = predictions.shape[0]
    ce = -np.sum(targets*np.log(predictions+1e-9))/N
    return ce

def classificationReport(targets,predictions,label,offset=3):
    precision, recall, fscore, support = score(targets, predictions,labels=label)
    t=Texttable()
    form={}
    form["title"]=['Label','Precision','Recall','FScore','Support']
    form["value"]=[]
    for i,l in enumerate(label):
        c=[str(l),str(precision[i]),str(recall[i]),str(fscore[i]),str(support[i])]
        form["value"].append(c)
    return form

def classificationReportTxt(targets,predictions,label,offset=3):
    precision, recall, fscore, support = score(targets, predictions,labels=label)
    t=Texttable()
    content=[['Label','Precision','Recall','FScore','Support']]
    for i,l in enumerate(label):
        c=[l,precision[i],recall[i],fscore[i],support[i]]
        content.append(c)
    t.add_rows(content)
    txtSplit=t.draw().split('\n')
    txtSplit=[" "*offset+tt for tt in txtSplit]
    txt=""
    for tt in txtSplit:
        txt+=(tt+"\n")
    return txt
