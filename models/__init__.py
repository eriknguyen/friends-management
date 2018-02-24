from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from os.path import dirname, basename, isfile
import glob


Model = declarative_base()

def init_database(engine):
    db_engine = create_engine(engine, echo=True)
    Model.metadata.create_all(db_engine)


""" Include all other model files """
modules = glob.glob(dirname(__file__)+"/*.py")
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and basename(f) != '__init__.py']
