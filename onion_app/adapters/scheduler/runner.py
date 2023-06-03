from typing import Optional, Callable
import logging.config

from onion_app.application.exceptions import InternalServerError

info_logger = logging.getLogger('info_logger')


class Scheduler:
    instance = None

    def __init__(self, task):
        self.__task = task

    @property
    def task(self):
        return self.__task

    @classmethod
    def get_instance(cls, task: Optional[Callable] = None):
        if not cls.instance:
            if not task:
                raise InternalServerError("Отсутствует ссылка на задачу исполняемую задачу")
            cls.instance = cls(task)
            return cls.instance
        return cls.instance

    async def execute(self):
        task = self.task
        if await task():
            info_logger.info('data was successfully uploaded!')
        else:
            info_logger.info('exceptions occurred!')
