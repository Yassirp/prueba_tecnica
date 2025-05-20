from sqlalchemy.orm import Session

class BaseRepository:
    def __init__(self, db: Session, model):
        self.db = db
        self.model = model

    def get_all(self, limit: int = None, offset: int = None, order_by: str = None, filters: dict = None):
        query = self.db.query(self.model)

        if filters:
            query =  self.filter_by(query, filters)

        if order_by:
           query = self.order_by(query, order_by)

        total = query.count()

        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)

        return query.all(), total

    
    def filter_by(self, query, filters: dict):
        for key, value in filters.items():
            if "__" in key:  # Handle relationships
                relation, column_name = key.split("__", 1)
                relation_attr = getattr(self.model, relation, None)
                if relation_attr is not None:
                    column = getattr(relation_attr.property.mapper.class_, column_name, None)
            else:  # Handle direct columns
                column = getattr(self.model, key, None)

            if column is not None and value is not None:
                if isinstance(value, str) and "%" in value:  # Handle LIKE filters
                    query = query.filter(column.ilike(value))
                else:
                    query = query.filter(column == value)
        return query
    
    def order_by(self, query, order_by: str):
            order_column, order_direction = order_by.split(":")
            column = getattr(self.model, order_column, None)
            if column is not None:
                if order_direction.lower() == "desc":
                    query = query.order_by(column.desc())
                else:
                    query = query.order_by(column.asc())
                    
            return query
        

    def get_by_id(self, id: int):
        return self.db.query(self.model).filter(self.model.id == id).first()


    def get_by_ids(self, ids: list[int]):
        return self.db.query(self.model).filter(self.model.id.in_(ids)).all()
    
    def create(self, data: dict):
        instance = self.model(**data)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def update(self, id: int, data: dict):
        instance = self.get_by_id(id)
        if not instance:
            return None

        for key, value in data.items():
            setattr(instance, key, value)

        self.db.commit()
        self.db.refresh(instance)
        return instance

    def delete(self, id: int):
        instance = self.get_by_id(id)
        if not instance:
            return None

        self.db.delete(instance)
        self.db.commit()
        return True
