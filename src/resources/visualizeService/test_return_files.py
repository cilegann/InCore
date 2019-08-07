from flask import Flask,make_response,abort
from flask_restful import Api,Resource,reqparse
class trf(Resource):
    def get(self):
        data=[]
        with open('./files/nlp.tsv','rb') as file:
            data.append(file.read())
        with open('./files/num.csv','rb') as file:
            data.append(file.read())
        return data,201