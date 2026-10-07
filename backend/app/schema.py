from typing import Literal
from pydantic import BaseModel, Field, ConfigDict

class TaskIn(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    priority: Literal["low", "medium", "high"] = "medium"
    done: bool = False

class TaskDone(BaseModel):
    done: bool
