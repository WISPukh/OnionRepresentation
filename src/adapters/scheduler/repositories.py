from typing import Optional, Callable

from adapters.scheduler.decorators import catch_exceptions
from exceptions import InternalServerError
import logging.config

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
            cls.instance = Scheduler(task)
            return cls.instance
        return cls.instance

    # @catch_exceptions(cancel_on_failure=True)
    async def execute(self):
        task = self.task
        if await task():
            info_logger.info('data was successfully uploaded!')
        else:
            info_logger.info('exceptions occurred!')
