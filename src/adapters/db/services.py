from sqlalchemy.sql import select
from application.interfaces import DB as BaseDB
from sqlalchemy.exc import SQLAlchemyError


class DB(BaseDB):

    async def get(self):
        return (await self.session_db.execute(select(self.model))).scalars().all()

    async def save(self, instances: list, report: str):
        try:
            self.session_db.add_all(instances)
            await self.session_db.commit()
        # TODO: change exceptions
        except SQLAlchemyError as e:
            report += f"{e} \n"
            return f"Some issues was occured: \n {report}"

        return f"All datas was completely loads: \n {report}"
