from sqlalchemy.sql import func
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    inspect,
)
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Server(Base):
    __tablename__ = "server"
    server_id = Column(Integer, primary_key=True)
    users = relationship("User", back_populates="server")


class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True)
    name = Column(String)
    money = Column(Integer, default=0)
    daily_tile = Column(DateTime(timezone=True), server_default=func.now())
    server_id = Column(Integer, ForeignKey("server.server_id"), nullable=False)
    server = relationship("Server", back_populates="users")


def connect_db():
    DATABASE_URL = "sqlite:///budget.db"  # Replace this with your database URL

    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    if not inspect(engine).has_table("Server"):
        Base.metadata.create_all(engine)
    return session


def server_exists(session, server_id):
    server = session.query(Server).filter_by(user_id=server_id).first()
    return server if server is not None else None
