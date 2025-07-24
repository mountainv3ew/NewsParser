import uuid

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    def model_dump(self):
        dictionary = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        dictionary['id'] = uuid.uuid4()
        return dictionary
