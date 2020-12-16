#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Created On: Sep 3rd, 2020
@Author: Smith Joshua 
@Email: joshua.smith.228@us.af.mil

@updated On:
@Updated By:
@Email:

@db_utils: A call to interface with the database and manage the connections and function calls. 


"""
import errno
import psycopg2
from collections import OrderedDict
from classes import db_entries


class db_connections(object):

    def __init__(self):
        self.connection = None
        self.name = "dump"
        self.username = "postgres"
        self.password = "abc123"
        self.host = "localhost"
        self.port = 5432

    def __del__(self):
        if self.connection is not None and self.connection.closed == 0:
            self.connection.close()

    def connect2db(self):
        """
            connects to a database and returns the connection

            Args:
                None
            Returns:
                (connection) An instance of the psycopg2 database connection.
        """
        if self.connection is None:
            self.get_credentials()
        try:
            self.connection = psycopg2.connect(
                "dbname={} user={} password={} host={} port={}".format(self.name, self.username, self.password,
                                                                       self.host, self.port))
        except(Exception, psycopg2.OperationalError) as er:
            print("Unable to connect to DB, please check credentials and that the DB is running. \nError: " + str(er))
        return self.connection

    def get_credentials(self):
        """
            gets the credentials from the user and sets the class variables.

            Args:
                None
            Returns:
                None
        """
        self.host = "localhost"  # input("Please enter the Host name:")
        self.name = "dump"  # input("Please enter the Database name:")
        self.port = "5432"  # input("Please enter the port number:")
        self.username = "postgres"  # input("Please enter the username:")
        self.password = "abc123"  # getpass()

    def populate_from_file(self, filename, table_name):
        """
             Takes entries from a file and inserts them into the database. For csv files the header must use the same
             naming convention as the database it is being inserted into. The table name must match the naming
             convention of the database as well.

             Args:
                 filename(string) The name of the file to use.
                 table_name(string) The name of the table to be inserted into.
             Return:
                 None
             Raises: OSError, IOError - In case the file doesnt exist or there is another error with the file access.
         """
        if ".csv" in filename:
            first_row = []
            try:
                with open(filename, 'r', encoding='utf-8-sig') as inputfile:
                    for line in inputfile:
                        line = line.strip()
                        if len(first_row) == 0:
                            first_row = line.split(",")
                        else:
                            entry = db_entries.db_table_entry(table_name, dict(zip(first_row, line.split(","))))
                            self.add(table_name, entry)
            except (OSError, IOError) as e:  # FileNotFoundError does not exist on Python < 3.3
                if getattr(e, 'errno', 0) == errno.ENOENT:
                    print("FileNotFoundError: " + str(e))
                else:
                    print(e)

    def execute_from_file(self, filename):
        """
            Executes SQL statements from a file. File expected to be in standard SQL statement layout.

            Args:
                filename(string) The name of the file to use.
            Return:
                None
            Raises: OSError, IOError - In case the file doesnt exist or there is another error with the file access.
        """
        try:
            with open(filename, 'r') as inputfile:
                to_execute = ""
                for line in inputfile:
                    if line != '\n':
                        to_execute += line
                        if ";" in line:
                            self.execute(to_execute)
                            to_execute = ""
        except (OSError, IOError) as e:  # FileNotFoundError does not exist on Python < 3.3
            if getattr(e, 'errno', 0) == errno.ENOENT:
                print("FileNotFoundError: " + str(e))
            else:
                print(e)

    def create_table(self, table_name, properties):
        """
            Creates a table in the database

            Args:
                table_name(string) The name of the table to be created.
                properties(dictionary) The dictionary of properties for the table. The format is name and type
                    Example: {"test_id":"INTEGER NOT NULL", "test_name": "VARCHAR(16)"}
            Return:
                None
        """
        sql = "CREATE TABLE {} (".format(table_name)
        index = len(properties) - 1
        for key, value in properties.items():
            sql += key + " " + value
            if index > 0:
                sql += ", "
            else:
                sql += ")"
            index -= 1
        self.execute(sql)

    def execute(self, command):
        """
            Sends a SQL statement to the database to be executed.

            Args:
                command(string) The SQL statement to be ran on the database.
            Returns:
                None
            Raises: psycopg2.DatabaseError - In case there is an error connecting  to the database.
        """
        if self.connection is None:
            self.connect2db()
        try:
            cur = self.connection.cursor()
            cur.execute(command)
            self.connection.commit()
            cur.close()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
            print(command)
            if self.connection is not None:
                cur = self.connection.cursor()
                cur.execute("ROLLBACK")
                self.connection.commit()
                cur.close()

    def add(self, table_name, entry):
        """
            Inserts values into a database.

            Args:
                table_name(string) The name of the table where the data will be added.
                entry(db_entries) The entry object to be added.

            Returns:
                None
        """
        sql = "INSERT INTO {}(".format(table_name)
        for key in entry.get_fields():
            if entry.values[key] is not None:
                sql += str(key) + ","
        sql = sql[:-1] + ") VALUES("
        for value in entry.get_values():
            if value is not None:
                if isinstance(value, str):
                    sql += "\'" + value + "\',"
                else:
                    sql += " " + str(value) + ","
        sql = sql[:-1] + ");"
        self.execute(sql)

    def update(self, table_name, search, entry):
        """
            Updates values in the database.
            Note: Does not check if the fields exist in the database.

            Args:
                table_name(string) The name of the table where the data will be updated.
                search(Dictionary) The dictionary of column(s) and the value(s) used to select the
                    correct record to change it.
                    Example: {"test_id" : 117}
                entry(db_entries) The entry object to update the db with

            Returns:
                None
        """
        sql = "Update {} SET ".format(table_name)
        for key, value in entry.values.items():
            if value is not None:
                if isinstance(value, str):
                    sql += key + " = \'" + value + "\',"
                else:
                    sql += key + " = " + str(value) + ","
        sql = sql[:-1] + " WHERE "
        index = len(search) - 1
        for key, value in search.items():
            if isinstance(value, str):
                sql += key + " = \'" + value + "\',"
            else:
                 sql += key + " = " + str(value) + ","
            if index > 0:
                sql = sql[:-1] + " AND "
            index -= 1
        sql = sql[:-1] + ";"
        self.execute(sql)

    def drop(self, table_name, search):
        """
            Deletes values in the database.
            Note: Does not check if the values exist in the database.

            Args:
                table_name(string) The name of the table where the data will be updated.
                search(Dictionary) The dictionary of column(s) and the value(s) used to select the
                    correct record to remove.
                    Example: {"test_id" : 007}
            Returns:
                None
        """
        sql = "DELETE FROM {} WHERE ".format(table_name)
        index = len(search) - 1
        for key, value in search.items():
            sql += key + " = \'" + str(value) + "\'"
            if index > 0:
                sql += " AND "
            index -= 1
        sql += ";"
        self.execute(sql)

    def retrieve(self, table_name, to_retrieve, count, additional_query=""):
        """
            Retrieves  values from the database.
            Note: Does not check if the fields exist in the database.

            Args:
                table_name(string) The name of the table where the data will be updated.
                to_retrieve([string]) The list of column(s) to be retrieved from the database.
                    Example: {"test_id", "test_name"}
                    * can only be used when pulling all fields from an existing table type
                count(int) The number of results to return.  (May modify this)
                    0 is all of the results
                    x is the first x results.
                additional_query(string) If additional  SQL statements are needed such as INNER JOIN and/or ORDER BY
                    Can be added as one continuous string or as a comment block.
            Returns:
                List of entries that were retrieved from the database.
        """
        if count < 0:
            return []
        sql = "SELECT "
        index = len(to_retrieve) - 1
        for item in to_retrieve:
            sql += item
            if index > 0:
                sql += ", "
            index -= 1
        sql += " FROM {} {}".format(table_name, additional_query)
        to_return = None
        cur = None
        try:
            cur = self.connection.cursor()
            cur.execute(sql)
            if count == 0:
                to_return = cur.fetchall()
            else:
                to_return = cur.fetchmany(count)
            cur.close()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        if to_return is None or len(to_return) == 0:
            return []
        entries = []
        for item in to_return:
            column_names = [desc[0] for desc in cur.description]
            table_dict = OrderedDict()
            for i in range(len(item)):
                table_dict[column_names[i]] = item[i]
            entries.append(db_entries.db_table_entry(table_name, table_dict))
        return entries