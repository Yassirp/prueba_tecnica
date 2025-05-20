from modules.CategoryModule.models.m_categories_regions import MCategoryRegion
from modules.CategoryModule.schemas.category_region_schema import MCategoryRegionCreate, MCategoryRegionUpdate
from modules.CategoryModule.repositories.category_region_repository import CategoryRegionRepository
from services.base_services import BaseService
from pydantic import ValidationError

class CategoryRegionService(BaseService):
    def __init__(self, db):
        self.repository = CategoryRegionRepository(db)
        super().__init__(
            MCategoryRegion,
            self.repository,
            MCategoryRegionCreate,
            MCategoryRegionUpdate
        )


    def get_subcategories_by_region(self, region_id: int, filters: dict = None):
        try:
            results = self.repository.get_one_with_relationships(region_id, filters)

            if not results:
                raise ValueError("No se encontró la región solicitada o no cumple con los filtros")

            # Extraer la información fija del primer resultado
            category_region, _, category, region = results[0]

            subcategories = []
            for _, subcategory, _, _ in results:
                subcategories.append({
                    "apu": subcategory.apu,
                    "category_id": subcategory.category_id,
                    "name": subcategory.name,
                    "unit": subcategory.unit,
                    "id": subcategory.id
                })

            region_data = {
                "id": category_region.id,
                "category": {
                    "id": category.id,
                    "name": category.name,
                },
                "region": {
                    "id": region.id,
                    "name": region.name,
                },
                "subcategory": subcategories
            }

            return region_data

        except ValidationError as ve:
            raise ValueError({
                "error": str(ve),
            })