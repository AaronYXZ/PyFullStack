import sqlite3

from flask import Flask, render_template, session, redirect, url_for, flash
from flask import request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
# from itemTable import table_generator
from Models.info import ModelInfo
from Models.result import ModelResult
from werkzeug import secure_filename

from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, length
import os
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"

bootstrap = Bootstrap(app)
moment = Moment(app)


@app.before_first_request
def create_tables():
    db.create_all()


class ModelForm(FlaskForm):
    modelName = StringField("Models Name [requried]", validators=[DataRequired()])
    modelDate = StringField("Models Date [required]", validators=[DataRequired()])
    modelVersion = StringField("Models Version")
    # model
    modelPath = StringField("Models Path", validators=[DataRequired()])
    # upload = FileField()
    modelDescription = TextAreaField("Description", validators=[length(200)])
    modelCategory = SelectField("Model Category",
                                choices=[('IE', "Information Extraction"), ("Class", "Classification"),
                                         ("Other", "Other")])
    submit = SubmitField("Submit")


@app.route("/log")
def log():
    # table = table_generator()
    # html = "<>"
    # return table_generator()
    return render_template('log.html')


@app.route("/model")
def model():
    return render_template('model.html')


@app.route("/", methods=["GET", "POST"])
def my_form_post():
    name = None
    date = None
    version = None
    path = None
    TAG = None
    Precision = None
    uploads = None
    form = ModelForm()
    if form.validate_on_submit():
        flash("Submission successful!")
        name = form.modelName.data
        date = form.modelDate.data
        version = form.modelVersion.data
        path = form.modelPath.data
        # uploadName = form.upload.name
        # uploadData = request.files(uploadName)
        # uploadName = secure_filename(form.upload.data.filename)
        wholePath = os.path.join(path, "training/output/avg-evaluation-results.txt")
        # wholePath = "/Users/aaronyu/Desktop/Project9_MLJ/Models/build1/training/output/avg-evaluation-results.txt"
        data = pd.read_table(wholePath)
        TAG = data.iloc[0, 0]
        Precision = data.iloc[0, 4]
        Recall = data.iloc[0, 5]
        F1 = data.iloc[0, 6]

        ## Create Model ModelInfo and save to database
        info = ModelInfo(name, path, date, version, "ie", "placeholder")
        info.save_to_db()

        form.modelName.data = ''
        form.modelPath.data = ''
        form.modelVersion.data = ''
        form.modelDate.data = ''
        # print(uploadData)

        return render_template('index.html', form=form)

    return render_template('index.html', form=form)


@app.route("/user/<name>")
def upload(name):
    return "<h1> hello , {}!</h1>".format(name)


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.errorhandler(404)
def internal_server_error(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    from db import db

    db.init_app(app)
    app.run(port=5000)
# app.run(debug=True)
