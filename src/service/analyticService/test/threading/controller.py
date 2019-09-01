from flask import Flask,make_response
from flask_restful import Api, Resource, reqparse
import glob
import logging
from core import core
import threading
import ctypes
import time

class controller(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('n', type=int,required=True)
        args = parser.parse_args()
        n=args['n']
        c=core(n)
        uid,tid=c.do()
        return make_response(str(uid)+" | "+str(tid))

class stop(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uid', type=str,required=True)
        args = parser.parse_args()
        uid=args['uid']
        for t in threading.enumerate():
            if t.name==uid:
                res=ctypes.pythonapi.PyThreadState_SetAsyncExc(t.ident, ctypes.py_object(SystemExit)) 
        if res==0:
            return make_response("TID not found")
        elif res!=1:
            return make_response("sth went wrong")
        return make_response("OK")