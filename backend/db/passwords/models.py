from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.types import TypeDecorator
from db.session import Base
from db.users.models import User


class HexByteString(TypeDecorator):
    """Convert Python bytestring to string with hexadecimal digits and back for storage."""

    impl = String

    def process_bind_param(self, value, dialect):
        if not isinstance(value, bytes):
            raise TypeError("HexByteString columns support only bytes values.")
        return value.hex()

    def process_result_value(self, value, dialect):
        return bytes.fromhex(value) if value else None


class Password(Base):
    __tablename__ = "passwords"

    pk = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(ForeignKey(User.user_id, ondelete='CASCADE'), nullable=False)
    service_name = Column(String, unique=True, nullable=False)
    password = Column(HexByteString, nullable=False)
