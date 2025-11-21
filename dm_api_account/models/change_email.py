from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ChangeEmail(BaseModel):
    model_config = ConfigDict(extra='forbid')
    login: Optional[str] = Field(None, description='User login')
    password: Optional[str] = Field(None, description='User password')
    email: Optional[str] = Field(None, description='New user email')
