from datetime import datetime

import faust

from config import settings
from db import SessionBuilder
from models.regex_settings import RegexSettings
from models.type_description import TypeDescription
from models.verification import Verification
from parser import SiteParser
from pdf_parser import create_text


class RawFileMessage(faust.Record, serializer="json"):
    file_name: bytes


app = faust.App(
    "file-processor-0",
    broker=settings.BOOTSTRAP_SERVER,
)

message_topic = app.topic(
    settings.MESSAGE_TOPIC,
    value_serializer=RawFileMessage,
)

site_parser = SiteParser()


@app.agent(message_topic)
async def on_raw_request(stream):
    async for msg_key, file_message in stream.items():
        file_path = f"{settings.FILE_DIR}/{file_message.file_name}"
        print(file_path)

        async with SessionBuilder() as session:
            regex_settings = await session.get(RegexSettings, 1)

            data = create_text(file_path, regex_settings)
            verifications = await site_parser.get_data(
                data["Номер_в_госреестре"][0].replace("-", "\-")
            )

            type_description = TypeDescription(
                gos_number=data["Номер_в_госреестре"][0],
                si_name=data["Наименование_СИ"][0],
                si_unit_of_measurement=data["Eденица_измерения_СИ"][0],
                si_measurement_error=data["Погрешностиь_СИ"][0],
                si_approval_date=datetime.strptime(data["Дата_утверждения_СИ"][0], "%Y-%M-%d").date(),
                si_producer=data["Производитель_СИ"][0],
                file_name=data["Наименование_файла_с_описанием"][0],
            )
            session.add(type_description)
            await session.commit()
            await session.refresh(type_description)
            for doc in verifications:
                print(doc)
                verification = Verification(
                    type_description_id=type_description.id,
                    si_modification=doc["mi.modification"],
                    si_type=doc["mi.mitype"],
                    si_verification_date=datetime.strptime(doc["valid_date"].split("T")[0], '%Y-%M-%d'),
                )
                session.add(verification)
            await session.commit()
