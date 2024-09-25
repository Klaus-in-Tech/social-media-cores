from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import CLOB, Boolean, Date, Identity, Column, Integer, String
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class Base(DeclarativeBase):
    pass

class Posts(Base):
    __tablename__ = "POSTS"


    id_identity = Identity(start=1, increment=1)
    id = Column(Integer, id_identity, primary_key=True)
    title = Column(String(50), unique=True, nullable=False)
    content = Column(CLOB,nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('SYSTIMESTAMP'))
    published = Column(Boolean,server_default='1',nullable=False)