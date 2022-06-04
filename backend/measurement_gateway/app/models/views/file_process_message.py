from pydantic import BaseModel


class VerificationView(BaseModel):
    file_name: str