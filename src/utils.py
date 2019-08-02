import logging
from params import params
import pymysql

def tokenValidator(string,token):
    logging.debug(f'[util token] Token str:{string} Token int:{token}')
    for i,s in enumerate(string):
        token-=(i+1)*ord(s)
    return (token==0)

class sql():
    def __init__(self):
        param=params()
        self.conn=pymysql.connect(param.dbhost,param.dbuser,param.dbpwd,param.dbschema)
        self.cursor=self.conn.cursor()
