from datetime import datetime, timezone

import faust
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from config import settings
from db import SessionBuilder
from model import predict
from models.application_area import ApplicationArea
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

            type_description = await session.execute(
                select(TypeDescription).where(
                    TypeDescription.gos_number == data["Номер_в_госреестре"][0]
                )
            )
            type_description = type_description.scalar_one_or_none()
            if not type_description:
                type_description = TypeDescription(
                    gos_number=data["Номер_в_госреестре"][0],
                    si_name=data["Наименование_СИ"][0],
                    si_unit_of_measurement=data["Eденица_измерения_СИ"][0],
                    si_measurement_error=data["Погрешностиь_СИ"][0],
                    si_measurement_error_type=data["Тип_погрешности"][0],
                    si_approval_date=datetime.strptime(
                        data["Дата_утверждения_СИ"][0], "%Y-%M-%d"
                    ).date(),
                    si_producer=data["Производитель_СИ"][0],
                    file_name=data["Наименование_файла_с_описанием"][0],
                    si_producer_country=data["Страна_производитель"][0],
                    si_purpose=data["Назначение_СИ"][0],
                )
            else:
                type_description.gos_number = (
                        type_description.gos_number or data["Номер_в_госреестре"][0]
                )
                type_description.si_name = (
                        type_description.si_name or data["Наименование_СИ"][0]
                )
                type_description.si_unit_of_measurement = (
                        type_description.si_unit_of_measurement
                        or data["Eденица_измерения_СИ"][0]
                )
                type_description.si_measurement_error = (
                        type_description.si_measurement_error or data["Погрешностиь_СИ"][0]
                )
                type_description.si_measurement_error_type = (
                        type_description.si_measurement_error_type
                        or data["Тип_погрешности"][0]
                )
                type_description.si_approval_date = (
                        type_description.si_approval_date
                        or datetime.strptime(
                    data["Дата_утверждения_СИ"][0], "%Y-%M-%d"
                ).date()
                )
                type_description.si_producer = (
                        type_description.si_producer or data["Производитель_СИ"][0]
                )
                type_description.file_name = (
                        type_description.file_name
                        or data["Наименование_файла_с_описанием"][0]
                )
                type_description.si_producer_country = (
                        type_description.si_producer_country
                        or data["Страна_производитель"][0]
                )
                type_description.si_purpose = (
                        type_description.si_purpose or data["Назначение_СИ"][0]
                )

            session.add(type_description)
            await session.commit()
            await session.refresh(type_description)

            application_area_name = predict(data["Назначение_СИ"][0])
            id = type_description.id

            application_area = await session.execute(
                select(ApplicationArea)
                    .where(ApplicationArea.application_area_name == application_area_name)
                    .options(selectinload(ApplicationArea.type_descriptions))
            )

            application_area = application_area.scalar_one_or_none()
            if not application_area:
                application_area = ApplicationArea(
                    application_area_name=application_area_name
                )

            application_area.type_descriptions.append(type_description)
            session.add(application_area)
            await session.commit()

            for doc in verifications:
                print(doc)
                verification = await session.execute(
                    select(Verification).where(
                        Verification.type_description_id == id
                        and Verification.si_verification_date
                        == datetime.fromisoformat(doc["verification_date"][:-1])
                    )
                )
                verification = verification.scalar_one_or_none()
                if not verification:
                    verification = Verification(
                        type_description_id=id,
                        si_modification=doc["mi.modification"],
                        si_type=doc["mi.mitype"],
                        si_verification_date=datetime.fromisoformat(
                            doc["verification_date"][:-1]
                        ).astimezone(timezone.utc),
                        si_verification_valid_until_date=datetime.fromisoformat(
                            doc["valid_date"][:-1]
                        ).astimezone(timezone.utc),
                    )
                else:
                    verification.type_description_id = verification.type_description_id or id
                    verification.si_modification = verification.si_modification or doc["mi.modification"]
                    verification.si_type = verification.si_type or doc["mi.mitype"]
                    verification.si_verification_date = verification.si_verification_date or datetime.fromisoformat(
                        doc["verification_date"][:-1]
                    ).astimezone(timezone.utc)
                    verification.si_verification_valid_until_date = verification.si_verification_valid_until_date or datetime.fromisoformat(
                        doc["valid_date"][:-1]
                    ).astimezone(timezone.utc)

                session.add(verification)
                await session.commit()
