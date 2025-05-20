class DataRegion:
    @staticmethod
    def from_model(region):
        return {
            "id": region.id,
            "name": region.name,
            "active": region.active
        }
