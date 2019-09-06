import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_fscore_support as score
from texttable import Texttable

def crossEntropy(predictions, targets, epsilon=1e-12):
    predictions = np.clip(predictions, epsilon, 1. - epsilon)
    N = predictions.shape[0]
    ce = -np.sum(targets*np.log(predictions+1e-9))/N
    return ce

def classificationReport(predictions,targets,offset=3):
    precision, recall, fscore, support = score(y_true, y_pred)
    t=Texttable()
    content=[['Label','Precision','Recall','FScore','Support']]
    for i in range(len(precision)):
        c=[str(i),precision[i],recall[i],fscore[i],support[i]]
        content.append(c)
    t.add_rows(content)
    txtSplit=t.draw().split('\n')
    txtSplit=[" "*offset+tt for tt in txtSplit]
    txt=""
    for tt in txtSplit:
        txt+=(tt+"\n")
    return txt
