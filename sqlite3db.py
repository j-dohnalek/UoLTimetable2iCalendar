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
import os.path

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
        conn = sqlite3.connect(db_file, timeout=2, isolation_level=None)
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

    con = None

    def __init__(self):
        """  Constructor """
        try:
            self.conn = sqlite3.connect(DBSRC, timeout=2)
        except Error as e:
            print(e)

    def execute(self, sql, args=()):
        """ execute insert update delete """
        if self.conn is None:
            raise ValueError("No sqlite connection")

        try:
            cur = self.conn.cursor()
            cur.execute(sql, args)
            self.conn.commit()
        finally:
            self.conn.close()

    def fetch(self, sql, args=()):
        """ execute select statements """
        result = None

        if self.conn is None:
            raise ValueError("No sqlite connection")

        try:
            cur = self.conn.cursor()
            cur.execute(sql, args)
            result = cur.fetchall()
        finally:
            self.conn.close()
            return result
