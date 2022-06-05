from pydantic import BaseModel


class FileProcessMessage(BaseModel):
    file_name: str