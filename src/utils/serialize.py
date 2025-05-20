def serialize_model(model):
    return {col.name: getattr(model, col.name) for col in model.__table__.columns}
