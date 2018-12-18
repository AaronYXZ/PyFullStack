# from itemTable import table_generator
import os
from flask import Flask, render_template, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from dbUtil import saveToDB
from Models.result import ModelResult

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"

bootstrap = Bootstrap(app)
moment = Moment(app)


@app.before_first_request
def create_tables():
    db.create_all()


class ModelForm(FlaskForm):
    modelName = StringField("Model Name [required]", validators=[DataRequired()])
    modelPath = StringField("Output Path [required]", validators=[DataRequired()])
    # modelPath = SearchField("Path")
    modelDate = DateField('Development Date', format='%Y-%m-%d')
    modelCategory = SelectField("Category",
                                choices=[('IE', "Information Extraction"), ("CLASS", "Classification"),
                                         ("OTHER", "Other")])
    modelVersion = SelectField("ML SDK Version",
                               choices=[('9.2', "9.2"), ("9.1", "9.1"),
                                        ("9.0", "9.0"), ("8.5", "8.5"), ("8.3", "8.3")])
    # model
    # upload = FileField()
    modelDescription = TextAreaField("Description")

    submit = SubmitField("Submit")


@app.route("/log")
def log():
    results = ModelResult.query.all()
    result1 = results[0]
    F1 = result1.F1
    return render_template("log.html", F1 = F1)


@app.route("/model")
def model():
    return render_template('model.html')


@app.route("/", methods=["GET", "POST"])
def my_form_post():
    # name = None
    # date = None
    # version = None
    # path = None
    # TAG = None
    # Precision = None
    # uploads = None
    form = ModelForm()
    if form.validate_on_submit():
        flash("Submission successful!")
        saveToDB(form)

        form.modelName.data = ''
        form.modelPath.data = ''
        form.modelDescription.data = ''
        form.modelVersion.data = ''
        form.modelDate.data = ''
        return render_template('index.html', form=form)

    return render_template('index.html', form=form)


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.errorhandler(404)
def internal_server_error(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    from db import db

    db.init_app(app)
    app.run(port=5002)
# app.run(debug=True)
