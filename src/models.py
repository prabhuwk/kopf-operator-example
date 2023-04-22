import logging
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from sqlalchemy import create_engine, select
from sqlalchemy.exc import NoResultFound

USER_DATABASE_NAME = "userdb"
USER_TABLE_NAME = "user_info"


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = USER_TABLE_NAME

    resource_name: Mapped[str] = mapped_column(String(30), primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    city: Mapped[str] = mapped_column(String(30))
    country: Mapped[str] = mapped_column(String(30))
    pincode: Mapped[int] = mapped_column()

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, resource_name={self.resource_name!r}, first_name={self.first_name!r}, last_name={self.last_name!r}, city={self.city!r}, country={self.country!r}, pincode={self.pincode!r})"


def create_database_engine():
    engine = create_engine(f"sqlite:///{USER_DATABASE_NAME}.sqlite", echo=True)
    Base.metadata.create_all(engine)
    return engine


def get_record_by_resource_name(engine, resource_name):
    logging.info(f"checking database entry for: {resource_name}")
    session = Session(engine)
    query = select(User).where(User.resource_name.is_(resource_name))
    try:
        result = session.scalars(query).one()
    except NoResultFound:
        result = None
    return result


def add_database_record(engine, record):
    with Session(engine) as session:
        logging.info(f"adding database entry for {record['resource_name']}")
        user_instance = User(**record)
        session.add(user_instance)
        session.commit()


def delete_database_record(engine, resource_name):
    logging.info(f"deleting database entry for: {resource_name}")
    session = Session(engine)
    found_resource = session.get(User, {"resource_name": resource_name})
    session.delete(found_resource)
    session.commit()
