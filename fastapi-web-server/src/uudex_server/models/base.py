from datetime import datetime
import pytz
from sqlalchemy import text, TIMESTAMP
from sqlmodel import SQLModel, Field

TZ_UTC = pytz.timezone("UTC")


class BaseModel(SQLModel):

    class Config:
        arbitrary_types_allowed = True


class TimeStampMixin(SQLModel):
    created_datetime: datetime | None = Field(
        sa_type=TIMESTAMP(timezone=True),
        sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")},
        nullable=False)
    updated_datetime: datetime | None = Field(
        sa_type=TIMESTAMP(timezone=True),
        sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")},
        nullable=False)


class ActiveSwitchMixin():
    active_sw: str = Field(default="Y")
