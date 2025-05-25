from pydantic import BaseModel
from typing import Optional

class EssayRequest(BaseModel):
    essay_text: str
    essay_theme: str
    essay_motivational_text: Optional[str] = None