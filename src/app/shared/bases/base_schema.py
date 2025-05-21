from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Any

class BaseOutSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.isoformat() if v else None
        },
        json_schema_extra={
            "example": {
                "created_at": "2024-03-14T12:00:00.000Z",
                "updated_at": "2024-03-14T12:00:00.000Z",
                "deleted_at": None
            }
        }
    )

    def model_dump(self, **kwargs) -> dict[str, Any]:
        data = super().model_dump(**kwargs)
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
        return data 