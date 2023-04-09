from app.database.db import db
from datetime import datetime, timedelta


def utc2local():
    return datetime.utcnow() - timedelta(hours=5)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    status = db.Column(db.String(20), nullable=False, default="todo")
    created_at = db.Column(
        db.DateTime, default=utc2local)
    updated_at = db.Column(
        db.DateTime, default=utc2local, onupdate=utc2local)

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
