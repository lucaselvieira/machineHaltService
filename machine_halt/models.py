from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class MachineHalt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    machine_tag = db.Column(db.String(24), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    reason = db.Column(db.String(128))
