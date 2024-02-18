from enum import Enum
from typing import Optional


class EdgeType(Enum):
    INSTANCE_OF = "InstanceOf"
    SUBCLASS_OF = "SubclassOf"
    HAS_ATTRIBUTE = "HasAttribute"
    HAS_INSTANCE = "HasInstance"
    SUPERCLASS_OF = "SuperclassOf"
    ATTRIBUTE_OF = "AttributeOf"
    MUTUALLY_EXCLUSIVE_WITH = "MutuallyExclusiveWith"

    @classmethod
    def from_string(cls, edge_type: str) -> Optional["EdgeType"]:
        return cls(edge_type)

    def __str__(self):
        return self.value
