from flask import render_template,url_for,Blueprint,flash
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import Form
from wtforms import StringField,SubmitField,FileField
from wtforms.validators import DataRequired
import os
from submitAnalyticAlgoChecker import algoChecker
import traceback
class formming(FlaskForm):
    jsonfile = FileField('\nStep 1. Json file: ',validators=[DataRequired(message="Can't be empty")])
    pyfile = FileField('\nStep 2. Python file:',validators=[DataRequired(message="Can't be empty")])
    submit=SubmitField("Upload and Run Test")

submitPage = Blueprint('simple_page', __name__)
@submitPage.route('/submit/<key>',methods=['GET','POST'])
def submit(key):
    with open('allowSubmit.csv') as file:
        lines=file.readlines()
    for line in lines:
        line=line.split(",")
        if key==line[1]:
            form=formming()
            if form.validate_on_submit():
                try:
                    jsonFile=form.jsonfile.data
                    pyFile=form.pyfile.data
                    jsonFileName=form.jsonfile.data.filename
                    pyFileName=form.pyfile.data.filename

                    if jsonFileName[:jsonFileName.rfind(".")]!=pyFileName[:pyFileName.rfind(".")]:
                        return 'We found some error in your submitted files, please fix it and upload again<br><br>----------ERROR REPORT BELOW----------<br>file name of json and py should be identical<br>---------------------------------------------------<br><br><a href="./'+key+'">upload again</a>'
                    if jsonFileName[jsonFileName.rfind("."):]!=".json" or pyFileName[pyFileName.rfind("."):]!='.py':
                        return ('We found some error in your submitted files, please fix it and upload again<br><br>----------ERROR REPORT BELOW----------<br>there should be a .json file and a .py file<br>---------------------------------------------------<br><br><a href="./'+key+'">upload again</a>')
                    jsonFileID=jsonFileName.split("_")[0]
                    pyFileID=pyFileName.split("_")[0]
                    if jsonFileID!=line[0] or pyFileID!=line[0]:
                        return ('We found some error in your submitted files, please fix it and upload again<br><br>----------ERROR REPORT BELOW----------<br>Filename format: studentID_algoname.py and studentID_algoname.json<br>---------------------------------------------------<br><br><a href="./'+key+'">upload again</a>')

                    jsonFile.save(os.path.join("tmp",form.jsonfile.data.filename))
                    pyFile.save(os.path.join("tmp",form.pyfile.data.filename))
                    result=algoChecker(form.jsonfile.data.filename,form.pyfile.data.filename)
                    if result!="success":
                        return ("We found some error in your submitted files, please fix it and upload again<br><br>----------ERROR REPORT BELOW----------<br>"+result+'<br><a href="./'+key+'">upload again</a>')
                    return 'Submit successfully. Your algo will appear at next hour'
                except Exception as e:
                    return "During parsing, some error occured, please notify us or try again later<br><br>----------ERROR MSG BELOW----------<br>"+traceback.format_exc()+"<br>---------------------------------------------------<br>"+'<br><a href="./'+key+'">upload again</a>'
            return render_template('submit.html',form=form)
    return "Not valid"