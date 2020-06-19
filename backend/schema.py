import graphene
from graphene import Mutation, ObjectType, List, Schema, String, Field
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ORM_models import Tag as Tag_model, Todo as Todo_model, Comment as Comment_model
from datetime import datetime
TEST_DATABASE_FP = "todo-data-test.sqlite3"
engine = create_engine(f"sqlite:///{TEST_DATABASE_FP}", echo=False)
conn   = engine.connect()
Session  = sessionmaker(bind=engine)

class Comment(ObjectType):
    id = String()
    description = String()
    create_timestamp = String()
    edit_timestamp = String()
    todo = Field(lambda :Todo)

class Tag(ObjectType):
    id = String()
    name = String()
    color = String()
    todos = List(lambda : Todo)

class Todo(ObjectType):
    id = String()
    description = String()
    done = String()
    create_timestamp = String()
    edit_timestamp = String()

    tags = List(Tag)
    comments = List(Comment)

class Query(ObjectType):
    find_todo = Field(Todo, id=String(required=True))
    all_todos = List(Todo)
    all_tags  = List(Tag)

    def resolve_find_todo(parent, info, id):
        return Session().query(Todo_model).filter_by(id=id).one_or_none()
    
    def resolve_all_todos(parent, info):
        return Session().query(Todo_model).all()        

    def resolve_all_tags(parent, info):
        return Session().query(Tag_model).all()


class CreateTodo(Mutation):
    class Arguments:
        description = String(required=True)

    status = String()
    result = Field(Todo)

    def mutate(root, info, description):
        try:
            session = Session()
            
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            todo = Todo_model(description=description, done="false", create_timestamp=now, edit_timestamp=now)
            session.add(todo)
            session.commit()
            return CreateTodo(status="OK", result=todo)

        except Exception as e:
            return CreateTodo(status=f"ERROR: {e}", result=None)


class Mutations(ObjectType):
    create_todo = CreateTodo.Field()

if __name__ == "__main__":
    from flask import Flask
    from flask_graphql import GraphQLView
    schema = Schema(query=Query, mutation=Mutations)

    app = Flask(__name__)
    app.debug = True
    app.add_url_rule('/', view_func=GraphQLView.as_view('graphql', schema = schema, graphiql=True))
    app.run()