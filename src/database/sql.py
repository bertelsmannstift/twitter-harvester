"""Relational database setup."""
import sqlalchemy
from utils.settings import get_settings

engine = sqlalchemy.create_engine(
    get_settings().sql_connection,
    pool_pre_ping=True,
)
