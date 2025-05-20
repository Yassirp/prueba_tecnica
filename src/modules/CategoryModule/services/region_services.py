from modules.CategoryModule.models.m_regions import MRegion
from modules.CategoryModule.repositories.region_repository import RegionRepository
from modules.CategoryModule.schemas.region_schema import RegionCreate, RegionUpdate
from services.base_services import BaseService

class RegionService(BaseService):
    def __init__(self, db):
        self.repository = RegionRepository(db)
        self.db = db
        super().__init__(MRegion, self.repository, RegionCreate, RegionUpdate)
        
