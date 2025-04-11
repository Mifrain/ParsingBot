from pydantic import BaseModel

class SiteInput(BaseModel):
    title: str
    url: str
    xpath: str
