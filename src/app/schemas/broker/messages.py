from pydantic import BaseModel


class TemplateMessageRequest(BaseModel):
    id: str

class TemplateMessageResponse(BaseModel):
    success: bool