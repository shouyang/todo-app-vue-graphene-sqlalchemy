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
        session = self.Session()
        todo_local = Todo(description="First Todo")

        session.add(todo_local)        
        session.commit()

        results = session.query(Todo).filter_by(description="First Todo")
        todo_query = results.first()

        self.assertEqual(results.count(), 1)
        self.assertEqual(todo_local.description, todo_query.description)
        self.assertEqual(todo_local.id, todo_query.id)
        
        self.assertEqual(todo_local, todo_query)
    
    def testTodoUpdate(self):
        session = self.Session()
        todo_local = Todo(description="Second Todo")

        session.add(todo_local)
        session.commit()

        results = session.query(Todo).filter_by(description="Second Todo")
        todo_query = results.first()

        todo_query.description = "Second Todo --Edited"
        session.add(todo_query)
        session.commit()

        self.assertEqual(todo_local.description, "Second Todo --Edited")
        self.assertEqual(todo_local.description, todo_query.description)
        self.assertEqual(todo_local.id, todo_query.id)
        
        self.assertEqual(todo_local, todo_query)

    def testTodoDelete(self):
        session = self.Session()
        todo_local = Todo(description="Third Todo")

        session.add(todo_local)
        session.commit()

        results = session.query(Todo).filter_by(description="Third Todo")
        self.assertEqual(results.count(), 1)

        session.delete(todo_local)
        session.commit()

        results = session.query(Todo).filter_by(description="Third Todo")
        self.assertEqual(results.count(), 0)

    def testTodoTag(self):
        session = self.Session()
        todo_local = Todo(description="Todo To be tagged")

        tagA_local  = Tag(name="A")
        tagB_local = Tag(name="B")

        todo_local.tags = [tagA_local, tagB_local]
        
        session.add(todo_local)
        session.commit()

        results = session.query(Todo).filter_by(description="Todo To be tagged")
        self.assertEqual(results.count(), 1)

        todo_query = results.first()
        self.assertEqual(todo_query.tags[0], tagA_local)
        self.assertEqual(todo_query.tags[1], tagB_local)

    def testTodoComment(self):
        session = self.Session()
        todo_local = Todo(description="Todo To be commented on")
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
