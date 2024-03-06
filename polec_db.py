from sqlalchemy import create_engine
from sqlalchemy import insert
from sqlalchemy import select, table, column
from sqlalchemy import MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.dialects.mysql import insert
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DATABASE_NAME = os.environ.get("DATABASE_NAME")
DATABASE_USER_NAME = os.environ.get("DATABASE_USER_NAME")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_SERVER = os.environ.get("DATABASE_SERVER")

engine = create_engine ('mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user = DATABASE_USER_NAME, password = DATABASE_PASSWORD, server = DATABASE_SERVER, database = DATABASE_NAME), future=True, pool_recycle=299)

metadata = MetaData(engine)
#Creating a configured session class
#https://www.geeksforgeeks.org/sqlalchemy-orm-creating-session/
Session = scoped_session(sessionmaker())
Session.configure(bind=engine)


def reading(value_name):

    table_obj = table('regions', 
                column('region_name'), 
                column('region_id')
                )
    table_obj_2 = table('var_id',
                column ('quarter'),
                column('var_id'),
                column ('value_name')
                )

    response_array = []
    session = Session()
    #creating session object
    with session:
        for row_1 in session.execute(select(table_obj)):
            for row_2 in session.execute(select(table_obj_2)):
                if row_2[2] == value_name:
                    response_array.append({row_1[0]: row_1[1]})
                    response_array.append({row_2[0]: row_2[1]})
        session.commit()
        # commit the session

    return  response_array


def writing (gross_values, write_table_name):
    table_obj = table(write_table_name,
                column('id'),
                column('year'),
                column('value'),
                column('quarter'),
                column('region')
        )
    
    session = Session()
    #creating session object

    with session:
    
        insert_stmt = insert(table_obj).values(gross_values)

        # INSERT…ON DUPLICATE KEY UPDATE (upsert) https://docs.sqlalchemy.org/en/20/dialects/mysql.html#insert-on-duplicate-key-update-upsert

        on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
            value = insert_stmt.inserted.value
            )
        session.execute(on_duplicate_key_stmt)
        session.commit()  
    # commit the session

def result_values(table_name):

    table_obj = table(table_name,
                column('year'),
                column('value'),
                column('quarter'),
                column('region')
        )
    result_array = []
    session = Session()
    #creating session object
    with session:
        for row in session.execute(select(table_obj)):
            result_array.append(row._asdict())
    return result_array

Session.remove()
#is called when the web request ends, usually by integrating with the web framework’s event system to establish an “on request end” event.
#https://docs.sqlalchemy.org/en/14/orm/contextual.html#sqlalchemy.orm.scoped_session.remove