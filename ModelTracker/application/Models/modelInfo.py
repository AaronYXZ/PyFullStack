from db import db


class ModelInfo(db.Model):
    ## referred http://flask-sqlalchemy.pocoo.org/2.3/models/
    # __table_name__ = "models"
    id = db.Column(db.Integer, primary_key=True)
    usecase_id = db.Column(db.Integer, db.ForeignKey("usecase_info.id"))
    usecaseName = db.relationship('UsecaseInfo',
                                 backref=db.backref('usecase_info', lazy=True))
    name = db.Column(db.String(80), unique=True)
    path = db.Column(db.String, unique=True, nullable=False)
    date = db.Column(db.DateTime)
    version = db.Column(db.String)
    category = db.Column(db.String)
    description = db.Column(db.String)

    # def __init__(self, name, path, date, version, category, description):
    #     self.name = name
    #     self.path = path
    #     self.date = date
    #     self.version = version
    #     self.category = category
    #     self.description = description

    def to_json(self):
        return {"name": self.name, "path": self.path, "date": self.date, "version": self.version,
                "category": self.category, "description": self.description}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
