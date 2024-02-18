from pathlib import Path

import pytest

from question_processor import QuestionProcessor


@pytest.fixture
# The path returned will be used as the data file for all tests in this scope
def question_processor_data_file() -> Path:
    return Path("data/ontology-huge.csv")


def test_timing_of_huge_ontology(
    question_processor: QuestionProcessor,
) -> None:
    question_processor.process("is baby grand a type of musical instrument?")

    assert True
