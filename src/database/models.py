from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from .db import Base


class Profile(Base):
    __tablename__ = "profile"

    user_id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)


class OldName(Base):
    __tablename__ = "old_names"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("profile.user_id"))
    name = Column(String)
    changed_at = Column(DateTime, default=datetime.now(timezone.utc))


class OldUsername(Base):
    __tablename__ = "old_usernames"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("profile.user_id"))
    username = Column(String)
    changed_at = Column(DateTime, default=datetime.now(timezone.utc))
