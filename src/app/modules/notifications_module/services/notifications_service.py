# Archivo generado autom�ticamente para notifications - services
from src.app.modules.notifications_module.models.notifications import Notification
from src.app.modules.notifications_module.schemas.notifications_schemas import NotificationOut
from src.app.modules.notifications_module.repositories.notifications_repository import NotificationsRepository
from src.app.shared.bases.base_service import BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Dict, Any, Tuple, List
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from src.app.shared.constants.messages import NotificationMessages

import os

class NotificationsService(BaseService[Notification, NotificationOut]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(
            model=Notification,
            repository_cls=NotificationsRepository,
            db_session=db_session,
            out_schema=NotificationOut,
        )
        self.db_session=db_session

    async def get_all(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Tuple[List[Dict[str, Any]], int]:
        try:
            
            stmt = select(self.model).options(
                selectinload(self.model.type_notification),
                selectinload(self.model.entity_document)
            )  

            if order_by:
                stmt = stmt.order_by(order_by)

            if offset:
                stmt = stmt.offset(offset)

            if limit:
                stmt = stmt.limit(limit)

            result = await self.db_session.execute(stmt)
            items = result.scalars().all()

            total = len(items)
            return items, total
        except Exception as e:
            raise e

    async def get_by_id(self, notification_id: int) -> NotificationOut:
        try:
            stmt = select(self.model).options(
                selectinload(self.model.type_notification),
                selectinload(self.model.entity_document)
            ).where(self.model.id == notification_id)

            result = await self.db_session.execute(stmt)
            item = result.scalar_one_or_none()

            if not item:
                raise HTTPException(status_code=404, detail=NotificationMessages.ERROR_NOT_FOUND)

            return item
        except Exception as e:
            raise e 
        
    async def create(self, notification: dict) -> NotificationOut:
        try:
            item = await self.repo.create(notification)
            return item
        except Exception as e:
            raise e
        
    async def update(self, notification_id: int, notification: dict) -> NotificationOut:
        try:
            item = await self.repo.update(notification_id, notification)
            return item
        except Exception as e:
            raise e

        
        