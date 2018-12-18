from db import db


class ModelResult(db.Model):
    ## referred http://flask-sqlalchemy.pocoo.org/2.3/models/
    __table_name__ = "results"
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey("model_info.id"))
    tag = db.Column(db.String)
    TP = db.Column(db.Numeric) ## Can't use db.Integer, sqlite store as binary b'\x13\x11\x00\x00\x00\x00\x00\x00'
    FP = db.Column(db.Numeric)
    FN = db.Column(db.Numeric)
    Precision = db.Column(db.Float(precision=2))
    Recall = db.Column(db.Float(precision=2))
    F1 = db.Column(db.Float(precision=2))

    def __init__(self, tag, TP, FP, FN, Precision, Recall, F1):
        self.tag = tag
        self.TP = TP
        self.FP = FP
        self.FN = FN
        self.Precision = Precision
        self.Recall = Recall
        self.F1 = F1

    def to_json(self):
        return {"tag": self.tag, "TP": self.TP, "FP": self.FP,  "FN": self.FN,
                "Precision": self.Precision, "Recall": self.Recall, "F1": self.F1}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
