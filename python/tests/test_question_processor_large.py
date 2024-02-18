from pathlib import Path

import pytest

from question_processor import QuestionProcessor
from question_result import QuestionResult


@pytest.fixture
# The path returned will be used as the data file for all tests in this scope
def question_processor_data_file() -> Path:
    return Path("data/ontology-large.csv")


def test_baby_grand_is_a_type_of_musical_instrument(
    question_processor: QuestionProcessor,
) -> None:
    assert QuestionResult.YES == question_processor.process(
        "is baby grand a type of musical instrument?"
    )


def test_smirnoff_is_a_drink(question_processor: QuestionProcessor) -> None:
    assert QuestionResult.YES == question_processor.process("is Smirnoff a drink?")


def test_cheddar_is_hard(question_processor: QuestionProcessor) -> None:
    assert QuestionResult.YES == question_processor.process(
        "is Cheddar considered to be hard?"
    )


@pytest.mark.parametrize(
    ["entity", "parent_class", "expected_result"],
    [
        ("Lassie", "mammal", QuestionResult.YES),
        ("dog", "animal", QuestionResult.YES),
        ("dog", "mammal", QuestionResult.YES),
        ("dog", "entity", QuestionResult.YES),
        ("dog", "dog", QuestionResult.YES),
        ("mammal", "animal", QuestionResult.YES),
        ("mammal", "entity", QuestionResult.YES),
        ("animal", "entity", QuestionResult.YES),
        ("potato", "food", QuestionResult.YES),
    ],
)
def test_instance_of_parent_class(
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
        ("dog", "entity", QuestionResult.YES),
        ("mammal", "animal", QuestionResult.YES),
        ("mammal", "entity", QuestionResult.YES),
        ("animal", "entity", QuestionResult.YES),
        ("Sherry", "drink", QuestionResult.YES),
        ("grand piano", "piano", QuestionResult.YES),
    ],
)
def test_subclass_of_parent_class(
    child_class: str,
    parent_class: str,
    expected_result: QuestionResult,
    question_processor: QuestionProcessor,
) -> None:
    assert expected_result == question_processor.process(
        f"is {child_class} a type of {parent_class}?"
    )


@pytest.mark.parametrize(
    ["entity", "attribute", "expected_result"],
    [
        ("Lassie", "four-legged", QuestionResult.YES),
        ("dog", "four-legged", QuestionResult.YES),
        ("mammal", "four-legged", QuestionResult.DONT_KNOW),
        ("animal", "four-legged", QuestionResult.DONT_KNOW),
        ("drink", "alcoholic", QuestionResult.DONT_KNOW),
        ("entity", "abstract", QuestionResult.DONT_KNOW),
        ("naan", "Indian", QuestionResult.YES),
    ],
)
def test_entity_has_attribute(
    entity: str,
    attribute: str,
    expected_result: QuestionResult,
    question_processor: QuestionProcessor,
) -> None:
    assert expected_result == question_processor.process(
        f"is {entity} considered to be {attribute}?"
    )
