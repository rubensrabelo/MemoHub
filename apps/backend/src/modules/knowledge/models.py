from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime


class Knowledge(SQLModel, table=True):
    __tablename__: str = "knowledge"

    id: int | None = Field(default=None, primary_key=True)
    question: str = Field(nullable=False)
    answer: str = Field(nullable=False)
    category: str = Field(max_length=100, nullable=False)
    favorite: bool = Field(default=False, nullable=False)
    
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            default=lambda: datetime.now(timezone.utc),
        )
    )

    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            default=lambda: datetime.now(timezone.utc),
            onupdate=lambda: datetime.now(timezone.utc),
        )
    )
