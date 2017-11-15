"""
SQLite database API 
Copyright (C) 2017 Jiri Dohnalek
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

# Function:
# Provide access to the database

# IMPORTS ##############################################################

from sqlite3 import Error
import sqlite3
import sys

########################################################################

DBSRC = 'cache.db'

# FUNCTIONS #############################################################

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file, timeout=2)
        return conn
    except Error as e:
        print(e)

    return None

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

# CLASSES ##############################################################

class DB:

    """ Connects to SQLite3 Database """

    __sql_create = """CREATE TABLE IF NOT EXISTS `event` (
                	`uid`	TEXT NOT NULL UNIQUE,
                	`start`	TEXT NOT NULL,
                	`end`	TEXT NOT NULL,
                	`name`	TEXT NOT NULL,
                	`room`	TEXT NOT NULL,
                	`timestamp`	INTEGER NOT NULL
                    );"""

    con = None

    def __init__(self):

        """  Constructor """
        # create a database connection
        conn = create_connection(DBSRC)
        if conn is not None:
            # create events table
            create_table(conn, self.__sql_create)
        else:
            print("Error! cannot create the database connection.")

        self.con = conn

    def execute(self, sql, args=()):
        """ execute insert update delete """

        if self.con is None:
            raise ValueError("No sqlite connection")

        try:
            cur = self.con.cursor()
            cur.execute(sql, args)
            self.con.commit()

        except lite.OperationalError:
            self.con.close()

        finally:
            self.con.close()

    def fetch(self, sql, args=()):
        """ execute select statements """
        result = None

        if self.con is None:
            raise ValueError("No sqlite connection")

        try:
            cur = self.con.cursor()
            cur.execute(sql, args)
            result = cur.fetchall()

        except lite.OperationalError:
            self.con.close()

        finally:
            self.con.close()
            return result
