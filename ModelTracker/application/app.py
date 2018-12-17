import sqlite3

from flask import Flask, render_template, session, redirect, url_for, flash
from flask import request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
# from itemTable import table_generator
from Models.info import ModelInfo
from Models.result import ModelResult

from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, FieldList
from wtforms.validators import DataRequired
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

class CV_score_form(FlaskForm):
    modelName = StringField("Models Name [requried]", validators=[DataRequired()])
    modelDate = StringField("Models Date [required]", validators=[DataRequired()])
    modelVersion = StringField("Models Version")
    # model
    modelPath = StringField("Models Path", validators=[DataRequired()])
    submit = SubmitField("Submit")
    uploads = FieldList(FileField())

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
    form = CV_score_form()
    if form.validate_on_submit():
        flash("Submission successful!")
        name = form.modelName.data
        date = form.modelDate.data
        version = form.modelVersion.data
        path = form.modelPath.data
        for upload in form.uploads.entries:
            uploads.append(upload)

        wholePath = os.path.join(path, "training/output/avg-evaluation-results.txt")
        # wholePath = "/Users/aaronyu/Desktop/Project9_MLJ/Models/build1/training/output/avg-evaluation-results.txt"
        data = pd.read_table(wholePath)
        TAG = data.iloc[0, 0]
        Precision = data.iloc[0, 4]
        Recall = data.iloc[0,5]
        F1 = data.iloc[0, 6]


        info = ModelInfo(name, path, date, version, "ie", "placeholder")
        info.save_to_db()

        # result = ModelResult()
        # result.save_to_db()

        # connection = sqlite3.connect("model.db")
        # cursor = connection.cursor()
        #
        # query = "INSERT INTO models VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)"
        # cursor.execute(query, (name, date, version, wholePath, Precision, Recall, F1))
        #
        # connection.commit()
        # connection.close()

        form.modelName.data = ''
        form.modelPath.data = ''
        form.modelVersion.data = ''
        form.modelDate.data = ''
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
    app.run(port = 5000)
# app.run(debug=True)
