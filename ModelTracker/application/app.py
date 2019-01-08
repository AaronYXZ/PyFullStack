# from itemTable import table_generator
import os
from flask import Flask, render_template, flash
from flask_bootstrap import Bootstrap
from flask_moment import Momentfk
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from dbUtil import saveToDB
from Models.result import ModelResult
from Models.info import ModelInfo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"

bootstrap = Bootstrap(app)
moment = Moment(app)


@app.before_first_request
def create_tables():
    db.create_all()


class ModelForm(FlaskForm):
    usecaseName = StringField("Usecase Name")  ## look in the path, if not provided, accept user input
    modelName = StringField("Model Name",
                            validators=[DataRequired()])  ## look in the path, if not provided, accept user input
    modelPath = StringField("Output Path [required]", validators=[DataRequired()])
    # modelPath = SearchField("Path")
    modelDate = DateField('Development Date', format='%Y-%m-%d')
    modelCategory = SelectField("Category",
                                choices=[('IE', "Information Extraction"), ("CLASS", "Classification"),
                                         ("OTHER", "Other")])
    modelVersion = StringField("ML SDK Version")
    # modelVersion = SelectField("ML SDK Version",
    #                            choices=[('9.2', "9.2"), ("9.1", "9.1"),
    #                                     ("9.0", "9.0"), ("8.5", "8.5"), ("8.3", "8.3")])
    # model
    # upload = FileField()
    modelDescription = TextAreaField("Description")

    submit = SubmitField("Submit")


@app.route("/log")
def log():
    results = ModelResult.query.join(ModelInfo, (ModelResult.model_id == ModelInfo.id)).all()
    cols = ["Model Name", "Date"]
    cols.extend(results[0].attri_to_list())

    rows = []
    for result in results:
        row = [result.model_info.name, result.model_info.date]
        row.extend(result.to_list())
        rows.append(row)

    return render_template("modelLogs.html", cols=cols, rows=rows)


@app.route("/model")
def model():
    return render_template('modelComponent.html')


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
        usecase = form.usecaseName.data
        form.usecaseName.data = usecase
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
