import unittest
import os
import shutil

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ORM_models import Todo, Comment, Tag

ORIGINAL_DATABASE_FP = "todo-data-original.sqlite3"
TEST_DATABASE_FP = "todo-data-test.sqlite3"

DELETE_TEST_DB_ON_END = False

class ORMTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        shutil.copyfile(ORIGINAL_DATABASE_FP, TEST_DATABASE_FP)
        self.engine = create_engine(f"sqlite:///{TEST_DATABASE_FP}", echo=False)
        self.conn   = self.engine.connect()
       
        self.Session  = sessionmaker(bind=self.engine)

    @classmethod
    def tearDownClass(self):
        self.conn.close()

        if DELETE_TEST_DB_ON_END:
            os.remove(TEST_DATABASE_FP)

    def testTodoCreate(self):
        description = "Check that todos can be created, saved and loaded again"

        session = self.Session()
        todo_local = Todo(description=description)

        session.add(todo_local)        
        session.commit()

        results = session.query(Todo).filter_by(description=description)
        todo_query = results.first()

        self.assertEqual(results.count(), 1)
        self.assertEqual(todo_local.description, todo_query.description)
        self.assertEqual(todo_local.id, todo_query.id)
        
        self.assertEqual(todo_local, todo_query)
    
    def testTodoUpdate(self):
        description = "Check that todos can be edited, saved and loaded again"

        session = self.Session()
        todo_local = Todo(description=description)

        session.add(todo_local)
        session.commit()

        results = session.query(Todo).filter_by(description=description)
        todo_query = results.first()

        todo_query.description = description
        session.commit()

        self.assertEqual(todo_local.description, description)
        self.assertEqual(todo_local.description, todo_query.description)
        self.assertEqual(todo_local.id, todo_query.id)
        
        self.assertEqual(todo_local, todo_query)

    def testTodoDelete(self):
        description = "Check that todos can be deleted"

        session = self.Session()
        todo_local = Todo(description=description)

        session.add(todo_local)
        session.commit()

        results = session.query(Todo).filter_by(description=description)
        self.assertEqual(results.count(), 1)

        session.delete(todo_local)
        session.commit()

        results = session.query(Todo).filter_by(description=description)
        self.assertEqual(results.count(), 0)

    def testTodoTag(self):
        description = "Check that todos can be tagged"

        session = self.Session()
        todo_local = Todo(description=description)

        tagA_local  = Tag(name="A")
        tagB_local = Tag(name="B")

        todo_local.tags = [tagA_local, tagB_local]
        
        session.add(todo_local)
        session.commit()

        results = session.query(Todo).filter_by(description=description)
        self.assertEqual(results.count(), 1)

        todo_query = results.first()
        self.assertEqual(len(todo_query.tags), 2)

    def testTodoComment(self):
        description = "Check that todos can be commented on"
        
        session = self.Session()
        todo_local = Todo(description=description)
        comment_local = Comment(description="An independent comment")

        todo_local.comments.append(comment_local)

        session.add(todo_local)
        session.commit()

        results = session.query(Comment).filter_by(description="An independent comment")
        self.assertEqual(results.count(), 1)

        comment_query = results.first()

        self.assertEqual(todo_local, comment_query.todo)

if __name__ == "__main__":
    unittest.main()
