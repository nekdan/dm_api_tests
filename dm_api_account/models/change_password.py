from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class ChangePassword(BaseModel):
    model_config = ConfigDict(extra='forbid')
    login: Optional[str] = Field(None, description='User login')
    token: Optional[UUID] = Field(None, description='Password reset token')
    oldPassword: Optional[str] = Field(None, description='Old password')
    newPassword: Optional[str] = Field(None, description='New password')
