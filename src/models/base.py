"""Declarative Base class to be used by SQLAlchemy database models."""

from typing import Any

from sqlalchemy.ext.declarative import declarative_base

Base: Any = declarative_base()
