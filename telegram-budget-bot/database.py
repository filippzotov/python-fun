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


class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True)
    name = Column(String)
    budget = Column(Integer, default=0)
    expenses = relationship("Expense", back_populates="user")


class Expense(Base):
    __tablename__ = "expense"
    expence_id = Column(Integer, primary_key=True)
    title = Column(String)
    amount = Column(Integer)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    user = relationship("User", back_populates="expenses")


def connect_db():
    DATABASE_URL = "sqlite:///budget.db"  # Replace this with your database URL

    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    if not inspect(engine).has_table("User"):
        Base.metadata.create_all(engine)
    return session


def user_exists(session, user_id):
    user = session.query(User).filter_by(user_id=user_id).first()
    return user if user is not None else None


def add_user(session, user_id, name, budget):
    new_user = User(user_id=user_id, name=name, budget=budget)
    session.add(new_user)
    session.commit()


def add_expense(session, title, user_id, amount):
    user = user_exists(session, user_id)
    if not user:
        return "User not created"
    new_expense = Expense(title=title, user_id=user.user_id, amount=amount)
    user.expenses.append(new_expense)

    session.commit()


def get_budget(session, user_id):
    user = user_exists(session, user_id)
    if not user:
        return None
    return user.budget


def get_money_left(session, user_id):
    user = user_exists(session, user_id)
    if not user:
        return None
    budget = user.budget
    expenses = user.expenses
    money_left = budget - sum([i.amount for i in expenses])
    return money_left


def get_user_expenses(session, user_id):
    user = user_exists(session, user_id)
    if not user:
        return None
    expenses = user.expenses
    expenses_text = ""
    for exp in expenses:
        expenses_text += f"{exp.title} - {exp.amount}\n"
    return expenses_text


def delete_user(session, user_id):
    user = user_exists(session, user_id)
    if not user:
        return None
    for expense in user.expenses:
        session.delete(expense)
    session.delete(user)
    session.commit()


session = connect_db()
# # add_user(session, 123, "bob", 50)
# add_expense(session, "phone", 123, 19)
# add_expense(session, "banana", 123, 3)
# print(get_budget(session, 123))
# print(get_money_left(session, 123))
