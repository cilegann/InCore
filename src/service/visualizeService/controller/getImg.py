from flask import Flask, make_response,abort
from flask_restful import Api,Resource,reqparse
from params import params
from utils import sql
import logging
import os

param=params()

class getImg(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('uid', type=str,required=True)
            parser.add_argument('action',type=str,required=True)
            args = parser.parse_args()
            logging.debug(f"[getImg] args: {args}")
            uid = args['uid']
            action=args['action']
            db=sql()
            db.cursor.execute(f"select `path` from plottedImgs where id='{uid}'")
            info=db.cursor.fetchall()
            info=[[tt for tt in t] for t in data]
            if len(info)==0:
                abort(404)
            path=info[0][0]
            file=open(path,'rb')
            data=file.read()
            response=make_response(data)
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
            if action=='download':
                response.headers['Content-Type']='application/octet-stream; charset=utf-8'
                response.headers['Content-Disposition'] = 'attachment; filename=test.png'
        except Exception as e:
            logging.error(f'[getImg] {e}')
            return {"status":"error","msg":str(e),"data":{}},400
        return response
        