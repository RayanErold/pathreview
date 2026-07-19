"""Schemas for webhook API requests and responses."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, HttpUrl, Field


class WebhookCreate(BaseModel):
    """Schema for creating a new webhook."""

    url: str = Field(..., description="Webhook callback URL")
    events: str = Field(
        default="review.completed",
        description="Comma-separated list of events to listen for",
    )
    secret: Optional[str] = Field(
        default=None, description="Optional secret for HMAC signature verification"
    )
    description: Optional[str] = Field(
        default=None, description="Optional description of the webhook"
    )


class WebhookUpdate(BaseModel):
    """Schema for updating an existing webhook."""

    url: Optional[str] = Field(default=None, description="New webhook callback URL")
    events: Optional[str] = Field(
        default=None, description="New comma-separated list of events"
    )
    secret: Optional[str] = Field(
        default=None, description="New secret for HMAC signature verification"
    )
    description: Optional[str] = Field(default=None, description="New description")
    is_active: Optional[bool] = Field(default=None, description="New active status")


class WebhookResponse(BaseModel):
    """Schema for webhook responses."""

    id: UUID
    url: str
    events: str
    is_active: bool
    secret: Optional[str] = None
    description: Optional[str] = None
    last_triggered_at: Optional[datetime] = None
    last_status_code: Optional[int] = None
    failure_count: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class WebhookListResponse(BaseModel):
    """Schema for webhook list responses."""

    items: list[WebhookResponse]
    total: int
    page: int
    page_size: int


class WebhookEventPayload(BaseModel):
    """Schema for webhook event payload sent to callback URL."""

    event: str = Field(..., description="Event name")
    webhook_id: str = Field(..., description="Webhook ID")
    timestamp: str = Field(..., description="ISO 8601 timestamp")
    data: dict = Field(..., description="Event-specific data")
