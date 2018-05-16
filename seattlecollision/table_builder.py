"""
This module generates the tables required for the project in the SQLite
database coll_data.db. It reads in a path containing the CSV files, and
then generates the required tables in the given database.
"""
from __future__ import print_function
import sqlite3
import csv
import os
import glob


def create_table(database, path):
    """
    This function takes as input a database, along with a path to a folder
    that contains CSV files. It then constructs tables in the given
    database, using the names of the CSV files. If the column name
    ends with _id, then an index is created on that column.

    :param database: This is the name of the database
    file to which the tables will be added.
    :param path: The path to a folder that contains a set of CSV files
    :return: Doesn't
    """
    db_obj = database

    conn = sqlite3.connect(db_obj)
    conn.text_factory = str
    if not os.path.exists(path):
        raise ValueError('The file path is not valid')
    col = conn.cursor()
    for csvfile in glob.glob(os.path.join(path, "*.csv")):
        tablename = os.path.splitext(os.path.basename(csvfile))[0]

        with open(csvfile, "r") as file:
            reader = csv.reader(file)

            header = True
            for row in reader:
                if header:
                    header = False

                    sql = "DROP TABLE IF EXISTS %s" % tablename
                    col.execute(sql)
                    sql = "CREATE TABLE %s (%s)" % (
                        tablename,
                        ", ".join(["%s text" % column for column in row]))
                    col.execute(sql)

                    for column in row:
                        if column.lower().endswith("_id"):
                            index = "%s__%s" % (tablename, column)
                            sql = "CREATE INDEX %s on %s (%s)" % (index, tablename, column)
                            col.execute(sql)

                    insertsql = "INSERT INTO %s VALUES (%s)" % (
                        tablename,
                        ", ".join(["?" for column in row]))

                    rowlen = len(row)
                else:
                    if len(row) == rowlen:
                        col.execute(insertsql, row)

            conn.commit()

    col.close()
    conn.close()
