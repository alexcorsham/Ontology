import io
from pathlib import Path

import pytest

from ontology.domain.ontology import Ontology
from ontology.exceptions.ontology_exceptions import InvalidEdgeTypeException
from question_processor import QuestionProcessor
from question_result import QuestionResult


@pytest.fixture
# The path returned will be used as the data file for all tests in this scope
def question_processor_data_file() -> Path:
    return Path("data/ontology.csv")


@pytest.mark.parametrize(
    ["entity", "attribute", "expected_result"],
    [
        ("hemlock", "poisonous", QuestionResult.YES),
        ("Lassie", "four-legged", QuestionResult.YES),
        ("Springer", "aquatic", QuestionResult.YES),
        ("Springer", "four-legged", QuestionResult.DONT_KNOW),
    ],
)
def test_is_considered_to_be(
    entity: str,
    attribute: str,
    expected_result: QuestionResult,
    question_processor: QuestionProcessor,
) -> None:
    assert expected_result == question_processor.process(
        f"is {entity} considered to be {attribute}?"
    )


@pytest.mark.parametrize(
    ["entity", "parent_class", "expected_result"],
    [
        ("Ginger", "animal", QuestionResult.YES),
        # We don't know the answer to this because we don't have any data on pets
        ("Lassie", "pet", QuestionResult.DONT_KNOW),
        # Another example of the incompleteness of our data - from the data we have, we only know that Clifford is an
        # animal, we do not know that he is a dog.
        ("Clifford the Big Red Dog", "animal", QuestionResult.YES),
        ("Clifford the Big Red Dog", "dog", QuestionResult.DONT_KNOW),
    ],
)
def test_is_instance(
    entity: str,
    parent_class: str,
    expected_result: QuestionResult,
    question_processor: QuestionProcessor,
) -> None:
    assert expected_result == question_processor.process(
        f"is {entity} a {parent_class}?"
    )


@pytest.mark.parametrize(
    ["child_class", "parent_class", "expected_result"],
    [
        ("dog", "animal", QuestionResult.YES),
        ("sequoia tree", "entity", QuestionResult.YES),
        # We don't know the answer because our data is incomplete - we may be missing a 'SubclassOf' edge between
        # 'pufferfish' and 'mammal', or it may be that this is false - we can't know purely based on our current data
        ("pufferfish", "mammal", QuestionResult.DONT_KNOW),
    ],
)
def test_is_subclass(
    child_class: str,
    parent_class: str,
    expected_result: QuestionResult,
    question_processor: QuestionProcessor,
) -> None:
    assert expected_result == question_processor.process(
        f"is {child_class} a type of {parent_class}?"
    )


# add more tests below here :)
@pytest.mark.parametrize(
    ["question", "expected_result"],
    [
        # this is valid, (head entity is 'this', tail entity is 'valid question')
        ("is this a valid question?", QuestionResult.DONT_KNOW),
        # these two are invalid since they don't fit the pattern
        ("who is the current president of the United States?", QuestionResult.INVALID),
        ("am I an instance of stupid?", QuestionResult.INVALID),
    ],
)
def test_invalid_question(
    question: str,
    expected_result: QuestionResult,
    question_processor: QuestionProcessor,
) -> None:
    assert expected_result == question_processor.process(question)


def test_invalid_edge_type_in_ontology(question_processor: QuestionProcessor) -> None:
    # Create a temporary in-memory CSV data
    csv_data = """\
    ID,EDGE_TYPE,HEAD_ENTITY,TAIL_ENTITY
    36,IsProbablyA,car,tree
    """

    # Convert the string data into a file-like object
    csv_file = io.StringIO(csv_data)

    # Pass the file-like object to the question processor
    with pytest.raises(InvalidEdgeTypeException):
        question_processor.ontology_facade.ontology = Ontology(csv_file)


@pytest.mark.parametrize(
    ["question", "expected_result"],
    [
        ("is Lassie a plant?", QuestionResult.NO),
        ("is Lassie a tree?", QuestionResult.NO),
    ],
)
def test_mutually_exclusive_with_condition(
    question: str,
    expected_result: QuestionResult,
    question_processor: QuestionProcessor,
) -> None:
    assert expected_result == question_processor.process(question)
