from extensions import db

class Device(db.Model):
    __tablename__ = "devices"

    id = db.Column(db.Integer, primary_key=True)
    device_code = db.Column(db.String, unique=True, nullable=False)
