from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import TypeVar, Generic, Any, Dict, Optional, Literal, Union

T = TypeVar("T")

class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class BaseOutSchema(BaseModel, Generic[T]):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={datetime: lambda v: v.isoformat() if v else None},
        json_schema_extra={
            "example": {
                "created_at": "2024-03-14T12:00:00.000Z",
                "updated_at": "2024-03-14T12:00:00.000Z",
                "deleted_at": None,
            }
        },
    )

    @classmethod
    def model_validate(
        cls,
        obj: Any,
        *,
        strict: Optional[bool] = None,
        from_attributes: Optional[bool] = None,
        context: Optional[Any] = None,
        by_alias: Optional[bool] = None,
        by_name: Optional[bool] = None,
    ) -> "BaseOutSchema[T]":
        return super().model_validate(
            obj,
            strict=strict,
            from_attributes=from_attributes,
            context=context,
            by_alias=by_alias,
            by_name=by_name,
        )

    def model_dump(
        self,
        *,
        mode: Union[Literal["json", "python"], str] = "python",
        include: Optional[Any] = None,
        exclude: Optional[Any] = None,
        context: Optional[Any] = None,
        by_alias: Optional[bool] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: Union[Literal["none", "warn", "error"], bool] = True,
        fallback: Optional[Any] = None,
        serialize_as_any: bool = False,
    ) -> Dict[str, Any]:
        return super().model_dump(
            mode=mode,
            include=include,
            exclude=exclude,
            context=context,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
            fallback=fallback,
            serialize_as_any=serialize_as_any,
        )
