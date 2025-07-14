from typing import Any
from abc import ABC, abstractmethod

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
