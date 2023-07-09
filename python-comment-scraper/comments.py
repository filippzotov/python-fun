import os
from glob import glob
import tokenize
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, select
from sqlalchemy.orm import sessionmaker, declarative_base


Base = declarative_base()


# File model for database
class File(Base):
    __tablename__ = "file"
    id = Column(Integer, primary_key=True)
    file_name = Column(String)


# Comment model for database
class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True)
    line_number = Column(Integer)
    text = Column(String)
    file_id = Column(Integer, ForeignKey("file.id"))


# Get all .py files from directory, default current directory
def get_file_names(directory="."):
    result = [y for x in os.walk(directory) for y in glob(os.path.join(x[0], "*.py"))]
    return result


# Returns all comments and line where comment appears from file_name
def get_comments_from_file(file_name):
    with open(file_name, "rb") as file:
        tokens = tokenize.tokenize(file.readline)
        comments = []
        for token in tokens:
            if token.type == tokenize.COMMENT:
                comments.append((token.start[0], token.string.strip()))
    return comments


# Creating database and returns session
def db_create():
    engine = create_engine("sqlite:///comments.db")
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)
    return session


def print_files_from_db(session, select_query):
    result = session.execute(select_query)
    print(result.all())


if __name__ == "__main__":
    session = db_create()
    files = get_file_names()
    for file in files:
        comments = get_comments_from_file(file)
        db_file = File(file_name=file)
        session.add(db_file)
        for comment in comments:
            db_comment = Comment(
                line_number=comment[0],
                text=comment[1],
                file_id=db_file.id,
            )
            session.add(db_comment)
    print_files_from_db(session, select(Comment))
