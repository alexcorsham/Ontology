from pathlib import Path

from logger import getLogger
from ontology.exceptions.ontology_exceptions import OntologyException
from ontology.facade import OntologyFacade
from question import Question, QuestionParsingException
from question_result import QuestionResult


class QuestionProcessor:
    logger = getLogger(__name__)
    data = {}

    def __init__(self, ontology_csv: Path):
        self.ontology_facade = OntologyFacade(ontology_csv)

    def process(self, input_question: str) -> QuestionResult:
        try:
            question = Question.from_string(input_question)
            self.logger.info(f"Processing valid question '{input_question}'")
            return self._process_question(question)
        except QuestionParsingException:
            self.logger.exception("Error processing question")
            return QuestionResult.INVALID

    def _process_question(self, question: Question) -> QuestionResult:
        try:
            return self.ontology_facade.process_question(question)
        except OntologyException as exception:
            self.logger.error("Error processing question: %s", exception.message)

        return QuestionResult.DONT_KNOW
