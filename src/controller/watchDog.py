from flask import Flask,make_response
from flask_restful import Api, Resource, reqparse
from params import params
import logging
import json
import importlib
import traceback

param=params()

class watchDog(Resource):
    def get(self):
        return 1