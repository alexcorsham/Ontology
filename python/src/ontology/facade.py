from pathlib import Path
from typing import Optional

from logger import getLogger
from ontology.domain.ontology import Ontology
from question import Question, QuestionType
from question_result import QuestionResult


class OntologyFacade:
    logger = getLogger(__name__)
    """
    This class is a facade for the ontology. It is responsible for creating the ontology and providing a way to access

    Reason for making this a facade:
        - I chose a pure python implementation for the ontology, but equally I could have chosen something else, e.g. owlready2, networkx or a graph database
        - If I chose to change the implementation of the ontology, no external calls to the facade would need to change since they are implemnentation agnostic
    """

    def __init__(self, file_path: Path):
        self.ontology = self.create_ontology(file_path)
        self.PROCESSING_METHODS_MAP = {
            QuestionType.INSTANCE_OF: self.ontology.is_instance_of,
            QuestionType.SUBCLASS_OF: self.ontology.is_subclass_of,
            QuestionType.HAS_ATTRIBUTE: self.ontology.has_attribute,
        }

    def create_ontology(self, file_path: Path):
        self.logger.info(f"Creating ontology from file {file_path}")
        return Ontology(file_path)

    def process_question(self, question: Question) -> QuestionResult:
        processing_method = self._get_processing_method(question)

        if not processing_method:
            self.logger.warn(f"No processing method found for question {question}")
            return QuestionResult.DONT_KNOW

        return processing_method(question.head, question.tail)

    # ---------------------------------------------------------------------------- #
    #                                    PRIVATE                                   #
    # ---------------------------------------------------------------------------- #
    def _get_processing_method(self, question: Question) -> Optional[callable]:
        question_type = question.get_type()

        return self.PROCESSING_METHODS_MAP.get(question_type)
