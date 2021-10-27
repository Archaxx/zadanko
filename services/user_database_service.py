from typing import Optional

import mysql.connector

from models.user import User


class UserDatabaseService:
    USER_TABLE = "user"

    def __init__(self):
        # TODO security
        self._mysql = mysql.connector.connect(host="localhost", user="user", password="user", database="zadanko")
        self._client = self._mysql.cursor()

    def get_user_by_name(self, username) -> Optional[User]:
        query = f"select * from {self.USER_TABLE} where username='{username}'"
        self._client.execute(query)
        if user := self._client.fetchone():
            return User(*user)
        return None

    def get_user_by_id(self, id_) -> Optional[User]:
        query = f"select * from {self.USER_TABLE} where id={id_}"
        self._client.execute(query)
        if user := self._client.fetchone():
            return User(*user)
        return None

    def create_user(self, body: dict):
        if not (username := body.get("username")) or self.get_user_by_name(username):
            raise ValueError
        keys = ", ".join(body.keys())
        values = "','".join(body.values())
        query = f"insert into {self.USER_TABLE} ({keys}) values ('{values}')"
        print(query)
        self._client.execute(query)
        self._mysql.commit()
