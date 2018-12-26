# from itemTable import table_generator
import os
from flask import Flask, render_template, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from dbUtil import saveToDB, saveUsecaseToDB
from Models.trainResult import TrainResult
from Models.modelInfo import ModelInfo
from Models.usecaseInfo import UsecaseInfo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Workfusion123'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"

bootstrap = Bootstrap(app)
moment = Moment(app)


@app.before_first_request
def create_tables():
    db.create_all()


class ModelForm(FlaskForm):
    modelName = StringField("Model Name",
                            validators=[DataRequired()])  ## look in the path, if not provided, accept user input
    modelPath = StringField("Output Path [required]", validators=[DataRequired()])
    modelDate = DateField('Development Date', format='%Y-%m-%d')
    modelVersion = StringField("ML SDK Version")
    # modelVersion = SelectField("ML SDK Version",
    #                            choices=[('9.2', "9.2"), ("9.1", "9.1"),
    #                                     ("9.0", "9.0"), ("8.5", "8.5"), ("8.3", "8.3")])
    modelDescription = TextAreaField("Description")

    submit = SubmitField("Submit")


class UsecaseForm(FlaskForm):
    usecaseName = StringField("Usecase Name")  ## look in the path, if not provided, accept user input
    usecaseDate = DateField('Create Date', format='%Y-%m-%d')
    usecaseCategory = SelectField("Category",
                                  choices=[('IE', "Information Extraction"), ("CLASS", "Classification"),
                                           ("OTHER", "Other")])
    usecaseDescription = TextAreaField("Description")

    submit = SubmitField("Submit")


@app.route("/log")
def log():
    results = TrainResult.query.join(ModelInfo, (TrainResult.model_id == ModelInfo.id)).all()
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


@app.route("/usecase")
def usecase():
    usecases = UsecaseInfo.query.all()
    return render_template('usecase.html', usecases=usecases)


@app.route("/usecase/create", methods=["GET", "POST"])
def usecaseCreate():
    form = UsecaseForm()
    if form.validate_on_submit():
        flash("Submission successful!")
        saveUsecaseToDB(form)
        form.usecaseName.data = ""
        form.usecaseDescription.data = ''
        form.usecaseDate.data = ''
        form.usecaseCategory.data = ''
        return render_template('usecase.html')

    return render_template('usecaseCreate.html', form=form)


@app.route("/usecase/<string:usecaseName>/LogModel", methods=["GET", "POST"])
def logModel(usecaseName):
    # models = UsecaseInfo.query.join(UsecaseInfo, (UsecaseInfo.id == ModelInfo.usecase_id)).filter_by(
    #     UsecaseInfo.usecaseName == usecaseName).all()
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
        return render_template('usecaseLogModel.html', form=form)

    return render_template('usecaseLogModel.html', form=form)

@app.route("/usecase/<string:usecaseName>/ShowModel")
def showModel(usecaseName):
    # models = UsecaseInfo.query.join(UsecaseInfo, (UsecaseInfo.id == ModelInfo.usecase_id)).filter_by(
    #     UsecaseInfo.usecaseName == usecaseName).all()
    return render_template('usecaseShowModel.html')


@app.route("/", methods=["GET", "POST"])
def homePage():
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


@app.route("/coll")
def coll():
    results = TrainResult.query.join(ModelInfo, (TrainResult.model_id == ModelInfo.id)).all()
    return render_template("collapsible.html", results=results)


if __name__ == '__main__':
    from db import db

    db.init_app(app)
    app.run(port=5002)
# app.run(debug=True)
