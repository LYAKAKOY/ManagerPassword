import uuid
from sqlalchemy import Column, String, UUID
from db.session import Base


class User(Base):
    __tablename__ = 'users'

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    login = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)