from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional, Any, Annotated

from pydantic import BaseModel, Field, ConfigDict, BeforeValidator


class PagingSettings(BaseModel):
    model_config = ConfigDict(extra='forbid')
    postsPerPage: Optional[int] = Field(None, description='Number of posts on a game room page')
    commentsPerPage: Optional[int] = Field(None, description='Number of commentaries on a game or a topic page')
    topicsPerPage: Optional[int] = Field(None, description='Number of detached topics on a forum page')
    messagesPerPage: Optional[int] = Field(
        None,
        description='Number of private messages and conversations on dialogue page'
    )
    entitiesPerPage: Optional[int] = Field(None, description='Number of other entities on page')


class ColorSchema(Enum):
    Modern = 'Modern'
    Pale = 'Pale'
    Classic = 'Classic'
    ClassicPale = 'ClassicPale'
    Night = 'Night'


class UserSettings(BaseModel):
    model_config = ConfigDict(extra='forbid')
    colorSchema: Optional[ColorSchema] = None
    nannyGreetingsMessage: Optional[str] = Field(
        None,
        description="Message that user's newbies will receive once they are connected",
    )
    paging: Optional[PagingSettings] = None


class BbParseMode(Enum):
    Common = 'Common'
    Info = 'Info'
    Post = 'Post'
    Chat = 'Chat'


class InfoBbText(BaseModel):
    model_config = ConfigDict(extra='forbid')
    value: Optional[str] = Field(None, description='Text')
    parseMode: Optional[BbParseMode] = None


class Rating(BaseModel):
    model_config = ConfigDict(extra='forbid')
    enabled: Optional[bool] = Field(None, description='Rating participation flag')
    quality: Optional[int] = Field(None, description='Quality rating')
    quantity: Optional[int] = Field(None, description='Quantity rating')


class UserRole(Enum):
    GUEST = 'Guest'
    PLAYER = 'Player'
    ADMINISTRATOR = 'Administrator'
    NANNY_MODERATOR = 'NannyModerator'
    REGULAR_MODERATOR = 'RegularModerator'
    SENIOR_MODERATOR = 'SeniorModerator'


def empty_string_to_none(value):
    return None if value == '' else value


InfoOrNone = Annotated[Optional[InfoBbText], BeforeValidator(empty_string_to_none)]


class UserDetails(BaseModel):
    model_config = ConfigDict(extra='forbid')
    login: Optional[str] = Field(None, description='Login')
    roles: Optional[List[UserRole]] = Field(None, description='Roles')
    mediumPictureUrl: Optional[str] = Field(None, description='Profile picture URL M-size')
    smallPictureUrl: Optional[str] = Field(None, description='Profile picture URL S-size')
    status: Optional[str] = Field(None, description='User defined status')
    rating: Optional[Rating] = None
    online: Optional[datetime] = Field(None, description='Last seen online moment')
    name: Optional[str] = Field(None, description='User real name')
    location: Optional[str] = Field(None, description='User real location')
    registration: Optional[datetime] = Field(
        None, description='User registration moment'
    )
    icq: Optional[str] = Field(None, description='User ICQ number')
    skype: Optional[str] = Field(None, description='User Skype login')
    originalPictureUrl: Optional[str] = Field(
        None, description='URL of profile picture original'
    )
    info: InfoOrNone = None
    settings: Optional[UserSettings] = None


class UserDetailsEnvelope(BaseModel):
    model_config = ConfigDict(extra='forbid')
    resource: Optional[UserDetails] = None
    metadata: Optional[Any] = Field(None, description='Additional metadata')
