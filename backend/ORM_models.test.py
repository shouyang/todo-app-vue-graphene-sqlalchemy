import unittest
import os
import shutil
from sqlalchemy import create_engine
import ORM_models

ORIGINAL_DATABASE_FP = "todo-data-original.sqlite3"
TEST_DATABASE_FP = "todo-data-test.sqlite3"

class ORMTestCase(unittest.TestCase):
    def setUp(self):
        shutil.copyfile(ORIGINAL_DATABASE_FP, TEST_DATABASE_FP)
        engine = create_engine(f"sqlite:///{TEST_DATABASE_FP}", echo=True)
        engine.connect()

    def tearDown(self):
        os.remove(TEST_DATABASE_FP)

    def testTodoCreate(self):
        pass
        
    

if __name__ == "__main__":
    unittest.main()
