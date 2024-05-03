from typing import List

import pydantic

from entities.enums import BaseEnum
from entities.qbase import QBaseModel


class EEntityTypes(BaseEnum):
    A = "a"
    B = "b"
    C = "c"
    D = "d"


class Attributes(QBaseModel):
    id: int | str = pydantic.Field(..., description="Attribute ID")
    name: str = pydantic.Field(..., description="Attribute Name")
    description: str | None = pydantic.Field(..., description="Attribute Description")
    default: str | None = pydantic.Field(..., description="Attribute Default Value Column")
    source: str = pydantic.Field(..., description="Attribute Source System")
    type: str | None = pydantic.Field(..., description="Attribute Type (e.g. string, int, float, date)")


class AttributeRequest(QBaseModel):
    """
    Request Parameters for Attributes Master Data
    """

    entity_type: EEntityTypes | None = pydantic.Field(description="Entity Type (A or B)", example=EEntityTypes.A)


class AttributeResponseList(QBaseModel):
    """
    Attributes Master Data
    """

    __root__: List[Attributes]
