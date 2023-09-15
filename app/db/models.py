from __future__ import annotations

import sys
import uuid

from sqlalchemy import (
    INT,
    Column,
    Float,
    String,
    ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils.types import UUIDType  # type: ignore


def _declarative_constructor_auto_instantiate_nested(self, **kwargs):
    """A simple constructor that allows initialization from kwargs.

    Sets attributes on the constructed instance using the names and
    values in ``kwargs``.

    Only keys that are present as
    attributes of the instance's class are allowed. These could be,
    for example, any mapped columns or relationships.

    EDITED by @scd75 to auto_instantiate nested lists' elements as child classes
    """
    cls_ = type(self)
    relationships = self.__mapper__.relationships
    for k in kwargs:
        if not hasattr(cls_, k):
            raise TypeError(
                "%r is an invalid keyword argument for %s" % (k, cls_.__name__)
            )
        if k in relationships.keys():
            if relationships[k].direction.name == "ONETOMANY":
                childclass = getattr(
                    sys.modules[self.__module__], relationships[k].argument
                )
                nestedattribute = getattr(self, k)
                for elem in kwargs[k]:
                    new_elem = childclass(**elem)
                    nestedattribute.append(new_elem)
        else:
            setattr(self, k, kwargs[k])


_declarative_constructor_auto_instantiate_nested.__name__ = "__init__"

Base = declarative_base(constructor=_declarative_constructor_auto_instantiate_nested)


class Computation(Base):
    __tablename__ = "computation"
    id: UUIDType = Column(UUIDType(), primary_key=True, default=uuid.uuid4)
    name: str = Column(String(255), nullable=True)
    parameter: int = Column(INT(), nullable=False)


class ComputationOutput(Base):
    __tablename__ = "computationOutput"
    id: UUIDType = Column(UUIDType(), primary_key=True, default=uuid.uuid4)
    value: float = Column(Float(), nullable=False)
    computed_by: UUIDType = Column(
        UUIDType(), ForeignKey("computation.id"), nullable=False
    )


