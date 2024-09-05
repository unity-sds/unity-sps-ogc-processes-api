from typing import Literal

from pydantic import BaseModel


class HealthCheck(BaseModel):
    status: Literal["OK"]
