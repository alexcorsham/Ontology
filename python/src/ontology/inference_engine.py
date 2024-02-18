from typing import Dict, List

from ontology.domain.entity import Entity
from ontology.domain.relationship import Relationship


class InferenceEngine:
    """
    An inference engine to infer relationships between entities.
    """

    def __init__(self, relationships: List[Relationship]):
        self.relationships = relationships
        self.head_index = self._index_relationships("head_entity")
        self.tail_index = self._index_relationships("tail_entity")

    def infer_relationships(self) -> None:
        """
        Infer relationships between entities based on the relationships provided.

        For example if we have the following relationships:
        - A --instance_of--> B
        - B --subclass_of--> C
        - C --has_attribute--> D

        The following relationships can be inferred (direct relationships):
        - A --instance_of--> C
        - A --has_attribute--> D
        - B --has_attribute--> D

        and the following inverse relationships (transitive) can be inferred (HasInstance, SuperClassOf, AttrbiuteOf):
        - C --has_instance--> A
        - C --superclass_of--> B
        - D --attribute_of--> A
        - D --attribute_of--> B
        - D --attribute_of--> C
        """
        inferred_relationships = []
        for relationship in self.relationships:
            inferred_relationships.extend(self._infer_relationships(relationship))

        # group by head entity
        inferred_relationships_index = self._index_relationships("head_entity")

        for entity, relationships in inferred_relationships_index.items():
            entity.add_relationships(relationships)

    def _index_relationships(
        self, entity_type: str
    ) -> Dict[Entity, List[Relationship]]:
        index = {}
        for relationship in self.relationships:
            entity = getattr(relationship, entity_type)
            if entity not in index:
                index[entity] = []
            index[entity].append(relationship)

        return index

    def _infer_relationships(self, relationship: Relationship) -> List[Relationship]:
        inferred_relationships = []
        inferred_relationships += self._infer_transitive_relationships(relationship)
        inferred_relationships += self._infer_direct_relationships(relationship)

        return inferred_relationships

    def _infer_direct_relationships(
        self, relationship: Relationship
    ) -> List[Relationship]:
        inferred_relationships = []
        if relationship.head_entity in self.tail_index:

            for rel in self.tail_index[relationship.head_entity]:
                inverse_relationship = rel.get_inverse()
                if not inverse_relationship:
                    continue

                inverse_relationship.set_is_inferred(True)

                inferred_relationships.append(inverse_relationship)

        return inferred_relationships

    def _infer_transitive_relationships(
        self, relationship: Relationship
    ) -> List[Relationship]:
        inferred_relationships = []
        # Add logic to infer transitive relationships, e.g. A --instance_of--> B, B --subclass_of--> C => A --instance_of--> C

        return inferred_relationships
