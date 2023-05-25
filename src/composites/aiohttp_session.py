from aiohttp import ClientSession


async def get_session() -> ClientSession:
    async with ClientSession() as session:
        yield session
