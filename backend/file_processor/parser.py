import aiohttp


class SiteParser:
    domain = "https://fgis.gost.ru/fundmetrology"
    data_template = (
        "{domain}/cm/xcdb/vri/select?fq=mi.mitnumber:*{number}*&q=*"
    )
    doc_number = 102141

    async def get_data(self, number: str):
        async with aiohttp.ClientSession() as session:
            request_link = self.data_template.format(
                domain=self.domain, number=number
            )
            async with session.get(request_link) as response:
                json = await response.json()
                return json["response"]["docs"]