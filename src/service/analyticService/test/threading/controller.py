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
        parser.add_argument('tid', type=int,required=True)
        args = parser.parse_args()
        tid=args['tid']
        for t in threading.enumerate():
            if t.ident==tid:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(SystemExit)) 
        time.sleep(5)
        print(threading.enumerate())
        return make_response("OK")