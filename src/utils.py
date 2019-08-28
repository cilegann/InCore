import logging
from params import params
import pymysql
import jwt

def tokenValidator(string,token):
    return jwt.decode(tokenstr, "iloveraid1", audience='www.inanalysis.com', algorithms=['HS256'])

class sql():
    def __init__(self):
        param=params()
        self.conn=pymysql.connect(param.dbhost,param.dbuser,param.dbpwd,param.dbschema)
        self.cursor=self.conn.cursor()
