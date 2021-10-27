import datetime
from enum import Enum
from typing import Optional

import mysql.connector

from models.task import Task


class Status(Enum):
    DONE = "done"
    NOT_DONE = "not done"


class TaskDatabaseService:
    TASK_TABLE = "task"

    def __init__(self):
        # TODO security
        self._mysql = mysql.connector.connect(host="localhost", user="user", password="user", database="zadanko")
        self._client = self._mysql.cursor()

    def get_task_by_id(self, id_: int) -> Optional[Task]:
        query = f"select * from {self.TASK_TABLE} where id={id_}"
        self._client.execute(query)
        if task := self._client.fetchone():
            return Task(*task)
        return None

    def get_task_for_user(self, user_id: int, **kwargs) -> list[Task]:
        query = f"select * from {self.TASK_TABLE} where "
        for key, value in kwargs.items():
            query += f"{key}='{value}' and "
        query += f"user_id={user_id}"
        self._client.execute(query)
        return [Task(*t) for t in self._client.fetchall() if t]

    def get_task_after_deadline(self) -> list[Task]:
        query = f"select * from {self.TASK_TABLE} " \
                f"where deadline<'{datetime.datetime.now()}' and status='{Status.NOT_DONE.value}'"
        self._client.execute(query)
        return [Task(*t) for t in self._client.fetchall() if t]

    def create_task(self, body: dict) -> None:
        if "status" in body:
            raise ValueError
        body.update({"status": Status.NOT_DONE.value,
                     "notified": False})
        keys = ", ".join(body.keys())
        values = ""
        for value in body.values():
            if isinstance(value, str):
                values += f"'{value}', "
            else:
                values += f"{value}, "
        values = values[:-2]
        query = f"insert into {self.TASK_TABLE} ({keys}) values ({values})"
        self._client.execute(query)
        self._mysql.commit()

    def delete_task(self, id_: int) -> None:
        query = f"delete from {self.TASK_TABLE} where id={id_}"
        self._client.execute(query)
        self._mysql.commit()

    def update_task(self, id_: int, body: dict) -> None:
        query = f"update {self.TASK_TABLE} set "
        values = ""
        for key, value in body.items():
            if isinstance(value, str):
                values += f"{key}='{value}' "
            else:
                values += f"{key}={value} "
        query += values
        query += f"where id={id_}"
        self._client.execute(query)
        self._mysql.commit()
