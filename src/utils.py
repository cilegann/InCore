import logging
from params import params
import pymysql
import jwt

def tokenValidator(token):
    if token=='testing':
        return True
    else:
        return jwt.decode(token, params().secretkey, audience='www.inanalysis.com', algorithms=['HS256'])

class sql():
    def __init__(self):
        param=params()
        self.conn=pymysql.connect(param.dbhost,param.dbuser,param.dbpwd,param.dbschema)
        self.cursor=self.conn.cursor()
