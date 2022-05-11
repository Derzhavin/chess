from sqlalchemy import create_engine
from .chessgame import metadata_obj


def init_engine(uri):
    engine = create_engine(uri)
    metadata_obj.create_all(engine)
    return engine
