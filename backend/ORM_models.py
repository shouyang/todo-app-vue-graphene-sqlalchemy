# coding: utf-8
from sqlalchemy import Column, Enum, ForeignKey, Integer, Table, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Tag(Base):
    __tablename__ = 'Tag'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    color = Column(Text)

    todos = relationship('Todo', backref="tags", secondary='Todo_Tag')


class Todo(Base):
    __tablename__ = 'Todo'

    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=False)
    done = Column(Text, nullable=False, default="false")
    create_timestamp = Column(Text)
    edit_timestamp = Column(Text)

    def __repr__(self):
        return f"Todo(id={self.id}, description={self.description}, done={self.done}, create_timestamp={self.create_timestamp}, edit_timestap={self.edit_timestamp})"

t_sqlite_sequence = Table(
    'sqlite_sequence', metadata,
    Column('name', NullType),
    Column('seq', NullType)
)


class Comment(Base):
    __tablename__ = 'Comment'

    id = Column(Integer, primary_key=True)
    todo_id = Column(ForeignKey('Todo.id'), nullable=False)
    description = Column(Text)
    create_timestamp = Column(Text)
    edit_timestamp = Column(Text)

    todo = relationship('Todo', backref="comments")


t_Todo_Tag = Table(
    'Todo_Tag', metadata,
    Column('todo_id', ForeignKey('Todo.id'), primary_key=True, nullable=False),
    Column('tag_id', ForeignKey('Tag.id'), primary_key=True, nullable=False)
)
