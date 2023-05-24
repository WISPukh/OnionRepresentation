from application.interfaces import SourceApi as BaseSourceApi


class SourceApi(BaseSourceApi):

    def get(self):
        headers = {'Authorization': f'Bearer {self.auth_api}'}
        url = self.base_url + f"?page_size={self.page_size}"

        response = await self.aiohttp_session.get(url=url, headers=headers)
        return await response.text()
