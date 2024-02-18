from __future__ import annotations

# Enable forward declarations
from typing import TYPE_CHECKING

from ontology.domain.edge_type import EdgeType
from ontology.exceptions.ontology_exceptions import InvalidEdgeTypeException

if TYPE_CHECKING:
    from entity import Entity  # Forward declaration to avoid circular dependency


class Relationship:
    """
    Represents a relationship between entities.
    """

    head_entity: Entity
    tail_entity: Entity
    edge_type: EdgeType
    is_inferred: bool

    def __init__(
        self,
        head_entity: Entity,
        tail_entity: Entity,
        edge_type: str,
        is_inferred: bool = False,
    ):
        self.head_entity = head_entity
        self.tail_entity = tail_entity
        self.edge_type = self.get_edge_type(edge_type)
        self.is_inferred = is_inferred

    def __str__(self):
        base_string = f"{self.head_entity} -- {self.edge_type} --> {self.tail_entity}"

        if self.is_inferred:
            base_string += " (inferred)"

        return base_string

    def get_edge_type(self, edge_type: str) -> EdgeType:
        try:
            edge_type_obj = EdgeType.from_string(edge_type)
        except ValueError:
            raise InvalidEdgeTypeException(f"Unknown edge type {edge_type}")

        return edge_type_obj

    def get_inverse(self) -> Relationship | None:
        """
        Get the inverse relationship of this relationship.
        """
        if self.is_instance_of():
            return Relationship(
                self.tail_entity,
                self.head_entity,
                EdgeType.HAS_INSTANCE,
            )
        elif self.is_subclass_of():
            return Relationship(
                self.tail_entity,
                self.head_entity,
                EdgeType.SUPERCLASS_OF,
            )
        elif self.is_has_attribute():
            return Relationship(
                self.tail_entity,
                self.head_entity,
                EdgeType.ATTRIBUTE_OF,
            )
        elif self.is_mutually_exclusive_with():
            return
        else:
            raise InvalidEdgeTypeException(f"Unknown edge type {self.edge_type}")

    def set_is_inferred(self, is_inferred: bool) -> None:
        self.is_inferred = is_inferred

    def is_instance_of(self) -> bool:
        return self.edge_type == EdgeType.INSTANCE_OF

    def is_subclass_of(self) -> bool:
        return self.edge_type == EdgeType.SUBCLASS_OF

    def is_has_attribute(self) -> bool:
        return self.edge_type == EdgeType.HAS_ATTRIBUTE

    def is_mutually_exclusive_with(self) -> bool:
        return self.edge_type == EdgeType.MUTUALLY_EXCLUSIVE_WITH
