from flask import render_template,url_for,Blueprint,flash
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import Form
from wtforms import StringField,SubmitField,FileField,BooleanField
from wtforms.validators import DataRequired
import os
from submitAnalyticAlgoChecker import algoChecker
import traceback
import logging
from utils import get_gpu_statistics
class formming(FlaskForm):
    jsonfile = FileField('\nStep 1. Json file: ',validators=[DataRequired(message="Can't be empty")])
    pyfile = FileField('\nStep 2. Python file:',validators=[DataRequired(message="Can't be empty")])
    checked=BooleanField("",validators=[DataRequired(), ])
    submit=SubmitField("Submit")

submitPage = Blueprint('simple_page', __name__)
def purgeTmp(jsonName,pyName):
    jsonFile=os.path.join("tmp",jsonName)
    pyFile=os.path.join("tmp",pyName)
    os.remove(jsonFile)
    os.remove(pyFile)
@submitPage.route('/submit/<key>',methods=['GET','POST'])
def submit(key):
    with open('allowSubmit.csv') as file:
        lines=file.readlines()
    idd=0
    for line in lines:
        line=line.split(",")
        if key==line[1].replace("\n",""):
            idd=line[0]
            break
    if idd==0:
        return render_template('404.html')
    form=formming()
    if form.validate_on_submit():
        logging.info(f"[SUBMIT] {idd} submitting")
        try:
            jsonFile=form.jsonfile.data
            pyFile=form.pyfile.data
            jsonFileName=form.jsonfile.data.filename
            pyFileName=form.pyfile.data.filename

            if jsonFileName[:jsonFileName.rfind(".")]!=pyFileName[:pyFileName.rfind(".")]:
                text='We found some error in your submitted files, please fix it and upload again<br><br>----------ERROR REPORT BELOW----------<br>file name of json and py should be identical<br>--------------------------------------------'
                try:
                    purgeTmp(form.jsonfile.data.filename,form.pyfile.data.filename)
                except:
                    pass
                return render_template('submit.html',form=form,alert=text,idd=idd,gpu_data=get_gpu_statistics())
            if jsonFileName[jsonFileName.rfind("."):]!=".json" or pyFileName[pyFileName.rfind("."):]!='.py':
                text='We found some error in your submitted files, please fix it and upload again<br><br>----------ERROR REPORT BELOW----------<br>there should be a .json file and a .py file<br>--------------------------------------------'
                try:
                    purgeTmp(form.jsonfile.data.filename,form.pyfile.data.filename)
                except:
                    pass
                return render_template('submit.html',form=form,alert=text,idd=idd,gpu_data=get_gpu_statistics())
            jsonFileID=jsonFileName.split("_")[0]
            pyFileID=pyFileName.split("_")[0]
            if jsonFileID.lower()!=idd or pyFileID.lower()!=idd:
                text='We found some error in your submitted files, please fix it and upload again<br><br>----------ERROR REPORT BELOW----------<br>Filename format: studentID_algoname.py and studentID_algoname.json<br>--------------------------------------------'
                try:
                    purgeTmp(form.jsonfile.data.filename,form.pyfile.data.filename)
                except:
                    pass
                return render_template('submit.html',form=form,alert=text,idd=idd,gpu_data=get_gpu_statistics())

            jsonFile.save(os.path.join("tmp",form.jsonfile.data.filename))
            pyFile.save(os.path.join("tmp",form.pyfile.data.filename))
            result=algoChecker(form.jsonfile.data.filename,form.pyfile.data.filename)
            if result!="success":
                text="We found some error in your submitted files, please fix it and upload again<br><br>----------ERROR REPORT BELOW----------<br>"+result
                try:
                    purgeTmp(form.jsonfile.data.filename,form.pyfile.data.filename)
                except:
                    pass
                return render_template('submit.html',form=form,alert=text,idd=idd,gpu_data=get_gpu_statistics())
            text='You have passed the basic test, submitted algorithm is now installed to the system.'
            logging.info(f"[SUBMIT] {idd} submitted: {jsonFileName[:jsonFileName.rfind('.')]}")
            return render_template('submit.html',form=form,success=text,idd=idd,gpu_data=get_gpu_statistics())
        except Exception as e:
            text="During parsing, some error occured, please notify us or try again later"
            try:
                purgeTmp(form.jsonfile.data.filename,form.pyfile.data.filename)
            except:
                pass
            return render_template('submit.html',form=form,alert=text,idd=idd)
    return render_template('submit.html',form=form,idd=idd,gpu_data=get_gpu_statistics())