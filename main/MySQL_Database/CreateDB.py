from typing import List
from venv import create
from mysql.connector import connect, Error
from sqlalchemy import create_engine
import pymysql
import pandas as pd
from typing import List

class CreateDB:

    def __init__(self, user: str, password: str, host: str='localhost'):

        self.host = host
        self.user = user
        self.password = password

    def __repr__(self):

        return "CreateDB Instance: host={0} and user={1}".format(self.host, self.user)
    
    def see_dbs(self):

        try:
            with connect(
                host=self.host,
                user=self.user,
                password=self.password
            ) as connection:
                with connection.cursor() as cursor:
                    show_query = "SHOW DATABASES"
                    cursor.execute(show_query)
                    for db in cursor:
                        print(db)
        except Error as e:
            print(e)

    def create_db(self, db_name: str):

        try:
            with connect(
                host=self.host,
                user=self.user,
                password=self.password
            ) as connection:
                create_query = "CREATE DATABASE {0}".format(db_name)
                with connection.cursor() as cursor:
                    cursor.execute(create_query)
        except Error as e:
            print(e)
    
    def commit_query(self, db_name: str, commit_query: str):

        try:
            with connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=db_name
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(commit_query)
                    connection.commit()
        except Error as e:
            print(e)

    def fetch_query(self, db_name: str, fetch_query: str) -> List:

        try:
            with connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=db_name
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(fetch_query)
                    result = cursor.fetchall()
                    return result
        except Error as e:
            print(e)

    def write_df(self, table_name: str, db_name: str, df: pd.DataFrame):
        
        try:
            engine = create_engine("mysql+pymysql://{user}:{password}@{host}/{db}".format(user=self.user, host=self.host, password=self.password, db=db_name))

            df.to_sql(table_name, engine, if_exists="append", index=False)
        
        except Error as e:
            print(e)



