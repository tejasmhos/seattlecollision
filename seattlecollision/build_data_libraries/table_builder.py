"""
This module takes the collidium_data.csv file and converts it into
a table that is placed in the given database file. The module is
called only once, during the initial setup process, and does not
need to be called anytime after.

Modules
    create_table: This module is responsible for creating a table.
    It takes as an argument, the name of the database, and the path
    to the CSV file.
"""
import os
import sqlite3
import pandas as pd


def create_table(database, path):
    """
    This function takes as input a database, along with a path to a folder
    that contains the CSV file. It then constructs a table in the given
    database, and completes its operation.

    :param database: This is the name of the database
    file to which the tables will be added.
    :param path: The path to a folder that contains the CSV file
    :return: Doesn't return anything
    """
    conn = sqlite3.connect(database)
    if not os.path.exists(path):
        raise ValueError('The file path is not valid')
    dataframe = pd.read_csv(path)
    del dataframe['Unnamed: 0']
    dataframe.to_sql('collidium_data', conn, if_exists='replace', index=False)
    conn.close()
