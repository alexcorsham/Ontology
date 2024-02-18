from typing import List

from logger import getLogger
from ontology.domain.relationship import Relationship


class Entity:
    """
    Class for representing an entity in the ontology and its relationships.
    """

    logger = getLogger(__name__)
    name: str
    relationships: List[Relationship]

    def __init__(self, name):
        self.name = name
        self.relationships = []

    def __str__(self):
        return self.name

    def add_relationship(self, relationship: Relationship) -> None:
        self.logger.debug(f"Adding relationship {relationship} to entity {self.name}")
        for rel in self.relationships:
            if (
                rel.head_entity == relationship.head_entity
                and rel.tail_entity == relationship.tail_entity
                and rel.edge_type == relationship.edge_type
            ):
                self.logger.debug(
                    f"Relationship {relationship} already exists for entity {self.name}"
                )
                return

        self.relationships.append(relationship)

    def add_relationships(self, relationships: List[Relationship]) -> None:
        for relationship in relationships:
            self.add_relationship(relationship)

    def get_relationships(self) -> List[Relationship]:
        return self.relationships
