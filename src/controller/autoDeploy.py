from flask import Flask
from flask_restful import Api, Resource, reqparse
import logging
import os

class gitPull(Resource):
    def post(self):
        try:
            os.system("git pull")
            logging.info("[GIT PULL] Done")
        except Exception as e:
            logging.error(f'[GIT PULL] {e}')