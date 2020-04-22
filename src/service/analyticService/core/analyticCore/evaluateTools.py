import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_fscore_support as score
from texttable import Texttable
import json


def classificationReport(targets,predictions,label,offset=3):
    precision, recall, fscore, support = score(targets, predictions,labels=label)
    t=Texttable()
    form={}
    form["title"]=['Label','Precision','Recall','FScore','Support']
    form["value"]=[]
    for i,l in enumerate(label):
        c=[str(l),str(round(precision[i],4)),str(round(recall[i],4)),str(round(fscore[i],4)),str(support[i])]
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

def cross_entropy( targets,predictions, epsilon=1e-12,indent=2):
    predictions = np.clip(predictions, epsilon, 1. - epsilon)
    N = predictions.shape[0]
    ce = -np.sum(targets*np.log(predictions+1e-9))/N
    return " "*indent+"cross_entropy: "+str(ce)+"\n"

def MAE(target,prediction,indent=2):
    return " "*indent+"MAE: "+str((np.abs(target-prediction)).mean())+"\n"

def MSE(target,prediction,indent=2):
    return " "*indent+"MSE: "+str(((target-prediction)**2).mean())+"\n"

def RMSE(target,prediction,indent=2):
    return " "*indent+"RMSE: "+str(np.sqrt(((target-prediction)**2).mean()))+"\n"
