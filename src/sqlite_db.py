
import sqlite3
import os
import typing


class SQLite:
  """
    # Example

    sqlite_db = SQLite("example_db")
    
    # make db
    sqlite_db.create_db()

    # create table
    query = '''CREATE TABLE example (NAME TEXT, POINTS INTEGER);'''
    sqlite_db.execute_query(query, commit=False)

    # insert table
    query = '''INSERT INTO example VALUES ('A', 1);'''
    result = sqlite_db.execute_query(query, commit=True)

    # read table
    query = '''SELECT * FROM example;'''
    result = sqlite_db.execute_query(query, commit=False)
    for i in result:
      print(i)
    
    # update table
    query = '''UPDATE example SET POINTS = 2 WHERE NAME='A';'''
    sqlite_db.execute_query(query, commit=True)

    # read updated table
    query = '''SELECT * FROM example;'''
    result = sqlite_db.execute_query(query, commit=False)
    for i in result:
      print(i)
    
    # delete table
    query = '''DELETE FROM example;'''
    sqlite_db.execute_query(query, commit=True)

    # read deleted table
    query = '''SELECT * FROM example;'''
    result = sqlite_db.execute_query(query, commit=False)
    for i in result:
      print(i)
    
    sqlite_db.close_db()
  """


  def __init__(self, db_address:str):
    self.db_address = db_address
    if os.path.isfile(db_address):
      try:
        self.conn = sqlite3.connect(self.db_address)
      except sqlite3.Error as e:
        print(e)
  
  
  def create_db(self):
    try:
      conn = sqlite3.connect(self.db_address)
    except sqlite3.Error as e:
      print(e)
    finally:
      if conn:
        conn.close()
        self.conn = sqlite3.connect(self.db_address)
  

  def execute_query(self, query:str, commit:bool):
    result = None

    try:
      result = self.conn.execute(query)
    except sqlite3.Error as e:
        print(e)
    
    if commit:
      self.conn.commit()
    if result:
      return result
  

  def close_db(self):
    if self.conn:
      self.conn.close()
  