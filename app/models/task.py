from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from sqlalchemy import DateTime
from datetime import datetime
from typing import Optional

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title : Mapped[str] = mapped_column() 
    description: Mapped[str] = mapped_column()
    completed_at : Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            # "is_complete": self.completed_at is not None
            "is_complete": bool(self.completed_at)
        }