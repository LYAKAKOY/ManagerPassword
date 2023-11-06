import uuid
from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    login = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)