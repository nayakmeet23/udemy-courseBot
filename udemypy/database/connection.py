from typing import Any
from abc import ABC, abstractmethod
from urllib.parse import urlparse

try:
    import mysql.connector
    MYSQL_AVAILABLE = True
    print("[Info] MySQL connector imported successfully")
except ImportError:
    MYSQL_AVAILABLE = False
    print("[Warning] Cannot use MySQL connector. To use MySQL, install mysql-connector-python")

try:
    import sqlite3
    print("[Info] SQLite imported successfully")
except ImportError as e:
    print("[Warning] Cannot use SQLite. To use SQLite, install sqlite3")


class DataBase(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def execute(self, query: str, commit: bool) -> Any:
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def reconnect(self):
        pass

    @abstractmethod
    def close(self):
        pass

    def execute_script(self, sql_script: str, commit: bool) -> Any:
        queries = sql_script.strip().split(";")
        output_list = []
        for query in queries:
            query = query.strip()
            if not query:
                continue
            try:
                output = self.execute(query, commit)
                output_list.extend(output or [])
            except Exception as exception:
                # Handle duplicate entry errors gracefully
                if "Duplicate entry" in str(exception) and "for key 'title'" in str(exception):
                    # Course already exists, skip silently
                    continue
                else:
                    # Other errors should still be reported
                    print(
                        "[Database] Could not execute query",
                        f"Error: {exception}",
                        f"SQL query:\n{query}",
                        sep="\n",
                    )
        return output_list


class MySqlDataBase(DataBase):  # ✅ Fix: Now inherits from DataBase
    def __init__(self, database_url: str):
        if not MYSQL_AVAILABLE:
            raise ImportError("MySQL connector not available. Install mysql-connector-python")
        self.database_url = database_url
        self.connect()

    def connect(self):
        dbc = urlparse(self.database_url)
        self.db = mysql.connector.connect(
            host=dbc.hostname,
            user=dbc.username,
            database=dbc.path.lstrip("/"),
            passwd=dbc.password,
        )

    def execute(self, query: str, commit: bool) -> Any:
        cursor = self.db.cursor()
        cursor.execute(query)
        try:
            result = cursor.fetchall()
        except:
            result = []
        if commit:
            self.commit()
        cursor.close()
        return result

    def commit(self):
        self.db.commit()

    def reconnect(self):
        self.db.reconnect()

    def close(self):
        self.db.close()


class Sqlite3DataBase(DataBase):
    def __init__(self, path: str):
        self.path = path
        self.connect()

    def connect(self):
        self.con = sqlite3.connect(self.path)

    def execute(self, query: str, commit: bool) -> Any:
        cursor = self.con.cursor()
        response = cursor.execute(query)
        if commit:
            self.commit()
        return response.fetchall()

    def commit(self):
        self.con.commit()

    def reconnect(self):
        self.close()
        self.connect()

    def close(self):
        self.con.close()
