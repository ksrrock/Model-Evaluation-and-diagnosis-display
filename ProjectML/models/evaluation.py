from db import db
from sqlalchemy.dialects.postgresql import JSON

class EvalModel(db.Model):
    __tablename__ = 'Evaluations'

    eval_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    model_type = db.Column(db.String(80))
    meta = db.Column(JSON)
    model_path = db.Column(db.String(80))
    dataset_path = db.Column(db.String(80))

    def __init__(self,name,model_type,model_path,dataset_path):
        self.name = name
        self.meta = {}
        self.model_type = model_type
        self.model_path = model_path
        self.dataset_path = dataset_path

    def json(self):
        return {"eval_id":self.eval_id,
        "name":self.name,
        "model_type":self.model_type,
        "metadata":self.meta,
        "model_path":self.model_path,
        "dataset_path":self.dataset_path}

    @classmethod
    def find_by_type(cls, type):
        return cls.query.filter_by(model_type=type)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(eval_id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()