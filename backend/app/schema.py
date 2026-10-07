from typing import Literal
from pydantic import BaseModel, Field , ConfigDict

class TaskIn(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    title: str = Field(min_length=1, max_length=120)
    priority: Literal["low", "medium", "high"] = "medium"

class TaskDone(BaseModel):
    done: bool
