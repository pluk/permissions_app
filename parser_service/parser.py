import asyncio
import aiohttp
import re
import json



class GooglePlayParser:
    __google_play_api_url = 'https://play.google.com/_/PlayStoreUi/data/batchexecute'

    __default_params = {
        'rpcids': 'xdSrCf',
        'f.sid': 4600557676402775172,
        'bl': 'boq_playuiserver_20190220.09_p0',
        'authuser': 0,
        'soc - app': 121,
        'soc - platform': 1,
        'soc - device': 1,
        '_reqid': 235968,
        'rt': 'c'
    }

    def __init__(self):
        self.__permissions_tokens_regexp = re.compile(r'\"(\[.*\\n)\"')

    async def get_permissions(self, app_id, hl):
        dirty_data = await self.get_dirty_response(app_id, hl)
        data = self.clear_data(dirty_data)

        permissions = self.parse_permissions(data)

        return permissions

    async def get_dirty_response(self, app_id, hl):
        params = self.__prepare_params(app_id, hl)

        async with aiohttp.ClientSession() as session:
            async with session.post(self.__google_play_api_url,
                                    data=params) as resp:
                data = await resp.read()
                return data.decode()

    def __prepare_params(self, app_id, hl):
        request_params = {
            'hl': hl,
            'f.req': '[[["xdSrCf","[[null,[\\"{}\\",7],[]]]",null,"vm96le:0|iA"]]]'.format(app_id)
        }
        return {**self.__default_params, **request_params}

    def clear_data(self, data):
        raw = self.__permissions_tokens_regexp.findall(data)
        json_data = raw[0].replace('\\n', '').replace('\\', '')
        return json.loads(json_data)

    def __parse_block(self, block):
        permissions = []
        for item in block:
            if not item:
                continue

            title = item[0]
            values = [i[1] for i in item[2]]
            picture = item[1][3][2]
            permissions.append(
                {'title': title, 'permissions': values, 'picture': picture}
            )

        return permissions

    def parse_permissions(self, data):

        perms = self.__parse_block(data[0])
        others = self.__parse_block(data[1])

        perms.append(self.parse_other(others, data))

        return perms

    def parse_other(self, others, data):
        if len(others) == 1:
            return others[0]

        for other in others[1:]:
            others[0]['permissions'] += other['permissions']

        others[0]['permissions'] += [i[1] for i in data[2]]

        return others[0]
