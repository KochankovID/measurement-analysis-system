import argparse
import asyncio
import math
import time

import aiofiles
import aiohttp
from tqdm import tqdm

loop = asyncio.get_event_loop()


class SiteParser:
    domain = "https://fgis.gost.ru/fundmetrology"
    data_template = (
        "https://fgis.gost.ru/fundmetrology/api/registry/4/data?pageNumber"
        "={page_number}&pageSize={page_size}&orgID=CURRENT_ORG"
    )
    doc_number = 102141

    def __init__(self, page_size: int):
        self._page_size = page_size

    async def run(self):
        for i in tqdm(range(1, math.ceil(self.doc_number / self._page_size))):
            async with aiohttp.ClientSession() as session:
                request_link = self.data_template.format(
                    page_number=i, page_size=self._page_size
                )
                async with session.get(request_link) as response:
                    json = await response.json()

                    request_files_jobs = []
                    for item in json["result"]["items"]:
                        link_property = next(
                            filter(
                                lambda x: x["title"] == "Описание типа",
                                item["properties"],
                            )
                        )
                        file_link = f'{self.domain}{link_property["link"]}'
                        file_name = link_property["value"]
                        request_files_jobs.append(
                            loop.create_task(get_file(session, file_link, file_name))
                        )

                    files = await asyncio.gather(*request_files_jobs)
                    save_files_jobs = [
                        loop.create_task(save_file(file)) for file in files
                    ]
                    await asyncio.gather(*save_files_jobs)
                    time.sleep(0.5)


async def get_file(session, link, file_name) -> dict[str, str]:
    async with session.get(link) as response:
        return {"file_name": file_name, "text": await response.read()}


async def save_file(file_data: dict[str, str]):
    f = await aiofiles.open(f'./files/{file_data["file_name"]}', mode="wb")
    await f.write(file_data["text"])
    await f.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set load params")
    parser.add_argument(
        "page_size",
        type=int,
        help="Number of items loaded in one request.",
    )
    args = parser.parse_args()
    site_parser = SiteParser(args.page_size)
    loop.run_until_complete(site_parser.run())
