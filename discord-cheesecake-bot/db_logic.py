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

import datetime

Base = declarative_base()


class Server(Base):
    __tablename__ = "server"
    server_id = Column(Integer, primary_key=True)
    users = relationship("User", back_populates="server")


class User(Base):
    __tablename__ = "user"
    inner_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    name = Column(String)
    money = Column(Integer, default=0)
    daily_time = Column(DateTime(timezone=True), server_default=func.now())
    server_id = Column(Integer, ForeignKey("server.server_id"), nullable=False)
    server = relationship("Server", back_populates="users")


def connect_db():
    DATABASE_URL = "sqlite:///servers.db"  # Replace this with your database URL

    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    if not inspect(engine).has_table("Server"):
        Base.metadata.create_all(engine)
    return session


def server_exists(session, server_id):
    server = session.query(Server).filter_by(server_id=server_id).first()
    return server if server is not None else None


def add_server(session, server_id):
    new_server = Server(server_id=server_id)
    session.add(new_server)
    session.commit()
    return new_server


def add_user(session, user_id, name, server):
    new_user = User(user_id=user_id, name=name, server_id=server.server_id)
    server.users.append(new_user)
    session.add(new_user)
    session.commit()


# 654302335522045972


def get_balance(session, user_id, server_id):
    user = session.query(User).filter_by(server_id=server_id, user_id=user_id).first()
    return user.money


def update_balance(session, user_id, server_id, money_change):
    user = session.query(User).filter_by(server_id=server_id, user_id=user_id).first()
    user.money += money_change
    session.commit()
    return user.money


def get_daily_time(session, user_id, server_id):
    user = session.query(User).filter_by(server_id=server_id, user_id=user_id).first()
    return user.daily_time


def update_daily_time(session, user_id, server_id):
    user = session.query(User).filter_by(server_id=server_id, user_id=user_id).first()
    now = datetime.datetime.now()
    difference = abs(user.daily_time - now).total_seconds() / 3600.0
    if difference < 8:
        difference = datetime.timedelta(hours=8 - difference)
        return (False, difference)
    user.daily_time = now
    session.commit()
    return (True, 0)


# session = connect_db()
# # update_balance(session, 654302335522045972, 714612336022781993, 500)
# ser = get_daily_time(session, 654302335522045972, 714612336022781993)
# res = now - ser
