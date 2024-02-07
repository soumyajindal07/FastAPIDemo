from typing import Optional
from pydantic import BaseModel

class ItemPayload(BaseModel):   
    item_name: str    