from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import CLOB, Date, Identity, Column, Integer, String

class Base(DeclarativeBase):
    pass

class Posts(Base):
    __tablename__ = "POSTS"

    id_identity = Identity(start=1, increment=1)
    id = Column(Integer, id_identity, primary_key=True)
    title = Column(String(50), unique=True, nullable=False)
    content = Column(CLOB,nullable=True)
    created_at = Column(Date,nullable=True)