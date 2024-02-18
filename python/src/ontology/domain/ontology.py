from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd

from logger import getLogger
from ontology.domain.entity import Entity
from ontology.domain.relationship import Relationship
from ontology.inference_engine import InferenceEngine
from question_result import QuestionResult


class Ontology:
    """
    Accessing information about the ontology happens through this class
    """

    entities: Dict[str, Entity] = {}
    logger = getLogger(__name__)

    def __init__(self, file_path: Path):
        self.load_entities(file_path)

    def load_entities(self, file_path: Path) -> None:
        dataframe = pd.read_csv(file_path)

        for _, row in dataframe.iterrows():
            edge_type = row.get("EDGE_TYPE")
            head_entity_name = row.get("HEAD_ENTITY")
            tail_entity_name = row.get("TAIL_ENTITY")

            head_entity = self.get_or_create_entity(head_entity_name)
            tail_entity = self.get_or_create_entity(tail_entity_name)

            relationship = Relationship(head_entity, tail_entity, edge_type)
            head_entity.add_relationship(relationship)

        self.infer_relationships()

    def infer_relationships(self) -> None:
        self.logger.info("Inferring relationships")
        relationships = self.get_all_relationships()

        InferenceEngine(relationships=relationships).infer_relationships()

    def get_or_create_entity(self, name) -> Entity:
        if name not in self.entities:
            self.entities[name] = Entity(name)

        return self.entities[name]

    def get_entity(self, name) -> Optional[Entity]:
        return self.entities.get(name)

    def get_entities(self) -> List[Entity]:
        return list(self.entities.values())

    def get_all_relationships(self) -> List[Relationship]:
        relationships = []
        for entity in self.entities.values():
            relationships.extend(entity.get_relationships())

        return relationships

    ...

    @lru_cache(maxsize=None)
    def is_instance_of(
        self, query_entity_name: str, target_entity_name: str
    ) -> QuestionResult:
        query_entity = self.get_entity(query_entity_name)
        target_entity = self.get_entity(target_entity_name)

        if query_entity is None or target_entity is None:
            return QuestionResult.DONT_KNOW

        if query_entity == target_entity:
            return QuestionResult.YES

        return self._check_instance_and_subclass(query_entity, target_entity)

    @lru_cache(maxsize=None)
    def is_subclass_of(
        self, query_entity_name: str, target_entity_name: str
    ) -> QuestionResult:
        query_entity = self.get_entity(query_entity_name)
        target_entity = self.get_entity(target_entity_name)

        if query_entity is None or target_entity is None:
            return QuestionResult.DONT_KNOW

        if query_entity == target_entity:
            return QuestionResult.YES

        return self._check_subclass(query_entity, target_entity)

    @lru_cache(maxsize=None)
    def has_attribute(
        self, query_entity_name: str, target_attribute_name: str
    ) -> QuestionResult:
        query_entity = self.get_entity(query_entity_name)
        target_attribute = self.get_entity(target_attribute_name)

        if query_entity is None or target_attribute is None:
            return QuestionResult.DONT_KNOW

        return self._check_has_attribute(query_entity, target_attribute)

    # ---------------------------------------------------------------------------- #
    #                                    PRIVATE                                   #
    # ---------------------------------------------------------------------------- #
    def _check_has_attribute(
        self, query_entity: Entity, target_attribute: Entity
    ) -> QuestionResult:
        stack = [query_entity]

        while stack:
            current_entity = stack.pop()
            for relationship in current_entity.get_relationships():
                if (
                    relationship.is_has_attribute()
                    and relationship.tail_entity == target_attribute
                ):
                    return QuestionResult.YES

                if relationship.is_instance_of() or relationship.is_subclass_of():
                    stack.append(relationship.tail_entity)

        return QuestionResult.DONT_KNOW

    def _check_subclass(
        self, query_entity: Entity, target_entity: Entity
    ) -> QuestionResult:
        stack = [query_entity]

        while stack:
            current_entity = stack.pop()
            for relationship in current_entity.get_relationships():
                if (
                    relationship.is_subclass_of()
                    and relationship.tail_entity == target_entity
                ):
                    return QuestionResult.YES
                if relationship.is_subclass_of():
                    stack.append(relationship.tail_entity)

        return QuestionResult.DONT_KNOW

    def _check_instance_and_subclass(
        self, query_entity: Entity, target_entity: Entity
    ) -> QuestionResult:
        stack = [query_entity]

        while stack:
            current_entity = stack.pop()
            for relationship in current_entity.get_relationships():
                if relationship.is_mutually_exclusive_with():
                    if relationship.tail_entity == target_entity:
                        return QuestionResult.NO

                    if (
                        self.is_subclass_of(
                            target_entity.name, relationship.tail_entity.name
                        )
                        == QuestionResult.YES
                    ):
                        return QuestionResult.NO

                if relationship.is_instance_of() or relationship.is_subclass_of():
                    if relationship.tail_entity == target_entity:
                        return QuestionResult.YES
                    stack.append(relationship.tail_entity)

        return QuestionResult.DONT_KNOW
