"""Tests for markdown parser."""

from pathlib import Path

import pytest

from text_to_qti.parser.markdown_parser import MarkdownParser
from text_to_qti.parser.question_models import QuestionType
from text_to_qti.utils.errors import ParseError


class TestMarkdownParser:
    """Tests for MarkdownParser class."""

    def test_parse_simple_mc_file(self, simple_mc_file: Path):
        """Test parsing a simple multiple choice file."""
        parser = MarkdownParser()
        quiz = parser.parse_file(str(simple_mc_file))

        assert quiz.metadata.title == "Simple Multiple Choice Quiz"
        assert len(quiz.questions) == 1
        assert quiz.questions[0].type == QuestionType.MULTIPLE_CHOICE
        assert len(quiz.questions[0].choices) == 4

    def test_parse_simple_tf_file(self, simple_tf_file: Path):
        """Test parsing a simple true/false file."""
        parser = MarkdownParser()
        quiz = parser.parse_file(str(simple_tf_file))

        assert quiz.metadata.title == "Simple True/False Quiz"
        assert len(quiz.questions) == 1
        assert quiz.questions[0].type == QuestionType.TRUE_FALSE

    def test_parse_mixed_questions(self, mixed_questions_file: Path):
        """Test parsing mixed question types."""
        parser = MarkdownParser()
        quiz = parser.parse_file(str(mixed_questions_file))

        assert len(quiz.questions) == 3
        assert quiz.questions[0].type == QuestionType.MULTIPLE_CHOICE
        assert quiz.questions[1].type == QuestionType.TRUE_FALSE
        assert quiz.questions[2].type == QuestionType.MULTIPLE_CHOICE

    def test_parse_question_with_feedback(self, simple_mc_file: Path):
        """Test that feedback is parsed correctly."""
        parser = MarkdownParser()
        quiz = parser.parse_file(str(simple_mc_file))

        question = quiz.questions[0]
        assert question.feedback is not None
        assert "capital" in question.feedback.lower()

    def test_parse_question_points(self, mixed_questions_file: Path):
        """Test that custom points are parsed correctly."""
        parser = MarkdownParser()
        quiz = parser.parse_file(str(mixed_questions_file))

        assert quiz.questions[2].points == 2

    def test_parse_file_not_found(self):
        """Test error handling for missing file."""
        parser = MarkdownParser()
        with pytest.raises(ParseError, match="File not found"):
            parser.parse_file("nonexistent.txt")

    def test_parse_content_no_questions(self):
        """Test error when no questions found."""
        parser = MarkdownParser()
        content = """---
title: Empty Quiz
---

This quiz has no questions.
"""
        with pytest.raises(ParseError, match="No questions found"):
            parser.parse_content(content)

    def test_parse_content_invalid_yaml(self):
        """Test error on invalid YAML."""
        parser = MarkdownParser()
        content = """---
title: Quiz
invalid yaml: [
---

## Question 1
[Type: multiple_choice]

Question?

a) Answer
*b) Correct
"""
        with pytest.raises(ParseError, match="Invalid YAML"):
            parser.parse_content(content)

    def test_parse_question_missing_type(self):
        """Test error when question type is missing."""
        parser = MarkdownParser()
        content = """## Question 1

What is the answer?

a) Answer 1
*b) Answer 2
"""
        with pytest.raises(ParseError, match="type not specified"):
            parser.parse_content(content)

    def test_parse_question_invalid_type(self):
        """Test error on invalid question type."""
        parser = MarkdownParser()
        content = """## Question 1
[Type: invalid_type]

What is the answer?

a) Answer 1
*b) Answer 2
"""
        with pytest.raises(ParseError, match="Invalid question type"):
            parser.parse_content(content)

    def test_metadata_with_defaults(self):
        """Test that metadata uses defaults correctly."""
        parser = MarkdownParser()
        content = """## Question 1
[Type: multiple_choice]

Question?

a) Answer
*b) Correct
"""
        quiz = parser.parse_content(content)
        assert quiz.metadata.title == "Untitled Quiz"
        assert quiz.metadata.points_per_question == 1

    def test_extract_correct_answer(self):
        """Test that correct answers are identified."""
        parser = MarkdownParser()
        content = """## Question 1
[Type: multiple_choice]

Question?

a) Wrong 1
b) Wrong 2
*c) Correct
d) Wrong 3
"""
        quiz = parser.parse_content(content)
        question = quiz.questions[0]
        correct_choices = [c for c in question.choices if c.is_correct]
        assert len(correct_choices) == 1
        assert correct_choices[0].letter == "c"
