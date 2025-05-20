from modules.ParameterModule.models.m_parameters_values import MParameterValue
from modules.ParameterModule.models.m_parameters import MParameter
from repositories.base_repository import BaseRepository

class ParameterValueRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, MParameterValue)


    def get_by_parameter_name(self, name):
        return (
            self.db.query(MParameterValue)
            .join(MParameterValue.getParameter)
            .filter(MParameter.name.ilike(f"%{name}%"))
            .all()
        )
        
    def get_by_parameter_references(self, references: list):
        return (
            self.db.query(MParameterValue)
            .join(MParameterValue.getParameter)
            .filter(MParameter.reference.in_(references))
            .all()
        )

    def get_by_parent_id(self, parent_id):
        return self.db.query(MParameterValue).filter(MParameterValue.parent_id == parent_id).all()

    def get_by_parent_ids(self, parent_ids: list):
        return self.db.query(MParameterValue).filter(MParameterValue.parent_id.in_(parent_ids)).all()

    def get_by_parameter_reference(self, reference):
        return (
            self.db.query(MParameterValue)
            .join(MParameterValue.getParameter)
            .filter(MParameter.reference == reference)
            .all()
        )

    def get_by_value_id(self, value_id):
        return self.db.query(MParameterValue).filter(MParameterValue.id == value_id).all()

    def get_by_value_reference(self, reference):
        return self.db.query(MParameterValue).filter(MParameterValue.reference == reference).all()

    def get_by_name(self, name):
        if not isinstance(name, list):
            name = [name]
        return self.db.query(MParameterValue).filter(MParameterValue.name.in_(name)).all()

    def get_by_parent_name(self, parent_name):
        return (
            self.db.query(MParameterValue)
            .join(MParameterValue.getParent)
            .filter(MParameter.name.ilike(f"%{parent_name}%"))
            .all()
        )
