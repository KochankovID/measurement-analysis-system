import io
import zipfile
from typing import List

import aiofiles
from app.containers import Container
from app.db.kafka import Kafka
from dependency_injector.wiring import Provide, inject
from fastapi import Depends, UploadFile
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette import status

from app.models.views.file_process_message import FileProcessMessage

router = InferringRouter()


@cbv(router)
class TypeDescriptionCBV:
    @router.post("/type_description/file_upload", status_code=status.HTTP_201_CREATED)
    @inject
    async def add_file(
            self,
            file: UploadFile,
            kafka: Kafka = Depends(Provide[Container.kafka]),
    ):
        async with aiofiles.open(f"files/{file.filename}", 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        await kafka.send_message("raw-files", FileProcessMessage(file_name=file.filename))

    @router.post("/type_description/zip_file_upload", status_code=status.HTTP_201_CREATED)
    @inject
    async def add_files(
            self,
            file: UploadFile,
            kafka: Kafka = Depends(Provide[Container.kafka]),
    ):
        with zipfile.ZipFile(io.BytesIO(await file.read()), 'r') as zip:
            names = zip.namelist()
            for name in names:
                async with aiofiles.open(f"files/{name}", 'wb') as out_file:
                    content = zip.read(name)
                    await out_file.write(content)
                await kafka.send_message("raw-files", FileProcessMessage(file_name=name))
