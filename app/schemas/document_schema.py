from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    filename: str
    content_text: str
    checksum: str
    size_bytes: int
    created_at: datetime | None = None
    updated_at: datetime | None = None


class DocumentUpdateRequest(BaseModel):
    filename: str | None = None
    content_text: str | None = None
