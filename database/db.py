import configparser
import pathlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

file_config = pathlib.Path(__file__).parent.parent.joinpath("config.ini")
config = configparser.ConfigParser()
config.read(file_config)

username = config.get("postgresql", "username")
password = config.get("postgresql", "password")
domain = config.get("postgresql", "domain")
db_name = config.get("postgresql", "db_name")

database_url = f"postgresql://{username}:{password}@{domain}:5432/{db_name}"

engine = create_engine(database_url, echo=False)
DBSession = sessionmaker(bind=engine)
session = DBSession()
