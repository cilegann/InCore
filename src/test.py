from resources.dataService.utils import getColType
import logging

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')
csvid='./files/num.csv'
tsvid='./files/nlp.tsv'
zipid='./files/cv'

def test_getColType():
    gct=getColType(csvid,'num').get()

if __name__=='__main__':
    test_getColType()