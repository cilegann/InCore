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
        uid=c.do()
        return make_response(str(uid))

class stop(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uid', type=str,required=True)
        args = parser.parse_args()
        uid=args['uid']
        res=0
        for t in threading.enumerate():
            if t.name==uid:
                tid=t.ident   
                res=ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(SystemExit)) 
        if res==0:
            return make_response("UID not found")
        elif res!=1:
            return make_response("sth went wrong")
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
        return make_response("OK")