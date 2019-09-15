from sqlite3db import DBSRC, create_connection, create_table
import sqlite3

if __name__ == '__main__':

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS `event` (
                	`uid`	TEXT NOT NULL UNIQUE,
                	`event_id`	TEXT NOT NULL,
                	`start`	TEXT NOT NULL,
                	`end`	TEXT NOT NULL,
                	`name`	TEXT NOT NULL,
                	`room`	TEXT NOT NULL,
                	`timestamp`	INTEGER NOT NULL
                    );
    """

    conn = create_connection(DBSRC)
    create_table(conn, create_table_sql)

    print 'Database created!'
