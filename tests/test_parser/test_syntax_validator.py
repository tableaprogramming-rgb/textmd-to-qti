"""Tests for syntax validator."""

import pytest
from pathlib import Path

from text_to_qti.parser.syntax_validator import SyntaxValidator
from text_to_qti.utils.errors import ValidationError


class TestSyntaxValidator:
    """Tests for SyntaxValidator class."""

    def test_validate_simple_mc_file(self, simple_mc_file: Path):
        """Test validating a simple multiple choice file."""
        validator = SyntaxValidator()
        # Should not raise
        validator.validate_file(str(simple_mc_file))

    def test_validate_simple_tf_file(self, simple_tf_file: Path):
        """Test validating a simple true/false file."""
        validator = SyntaxValidator()
        # Should not raise
        validator.validate_file(str(simple_tf_file))

    def test_validate_mixed_questions(self, mixed_questions_file: Path):
        """Test validating mixed question types."""
        validator = SyntaxValidator()
        # Should not raise
        validator.validate_file(str(mixed_questions_file))

    def test_validate_file_not_found(self):
        """Test error handling for missing file."""
        validator = SyntaxValidator()
        with pytest.raises(ValidationError, match="File not found"):
            validator.validate_file("nonexistent.txt")

    def test_validate_content_no_questions(self):
        """Test error when no questions found."""
        validator = SyntaxValidator()
        content = """---
title: Empty Quiz
---

This quiz has no questions.
"""
        with pytest.raises(ValidationError, match="No questions found"):
            validator.validate_content(content)

    def test_validate_invalid_yaml(self):
        """Test error on invalid YAML."""
        validator = SyntaxValidator()
        content = """---
title: Quiz
invalid: [unclosed
---

## Question 1
[Type: multiple_choice]

Question?

a) Answer
*b) Correct
"""
        with pytest.raises(ValidationError, match="Invalid YAML"):
            validator.validate_content(content)

    def test_validate_missing_question_type(self):
        """Test error when question type is missing."""
        validator = SyntaxValidator()
        content = """## Question 1

What is the answer?

a) Answer 1
*b) Answer 2
"""
        with pytest.raises(ValidationError, match="No question type specified"):
            validator.validate_content(content)

    def test_validate_invalid_question_type(self):
        """Test error on invalid question type."""
        validator = SyntaxValidator()
        content = """## Question 1
[Type: essay_question]

What is the answer?

a) Answer 1
*b) Answer 2
"""
        with pytest.raises(ValidationError, match="Invalid question type"):
            validator.validate_content(content)

    def test_validate_no_answer_choices(self):
        """Test error when no answer choices found."""
        validator = SyntaxValidator()
        content = """## Question 1
[Type: multiple_choice]

What is the answer?

No answer choices here!
"""
        with pytest.raises(ValidationError, match="No answer choices found"):
            validator.validate_content(content)

    def test_validate_no_correct_answer(self):
        """Test error when no correct answer marked."""
        validator = SyntaxValidator()
        content = """## Question 1
[Type: multiple_choice]

Question?

a) Answer 1
b) Answer 2
c) Answer 3
"""
        with pytest.raises(ValidationError, match="No correct answer"):
            validator.validate_content(content)

    def test_validate_non_sequential_letters(self):
        """Test error on non-sequential answer letters."""
        validator = SyntaxValidator()
        content = """## Question 1
[Type: multiple_choice]

Question?

a) Answer 1
c) Answer 2
*d) Answer 3
"""
        with pytest.raises(ValidationError, match="sequential"):
            validator.validate_content(content)

    def test_validate_tf_wrong_count(self):
        """Test error when true/false has wrong number of choices."""
        validator = SyntaxValidator()
        content = """## Question 1
[Type: true_false]

Is this true?

a) True
*b) False
c) Maybe
"""
        with pytest.raises(ValidationError, match="exactly 2 choices"):
            validator.validate_content(content)

    def test_validate_mc_multiple_correct(self):
        """Test error when multiple choice has multiple correct answers."""
        validator = SyntaxValidator()
        content = """## Question 1
[Type: multiple_choice]

Question?

*a) Answer 1
*b) Answer 2
c) Answer 3
"""
        with pytest.raises(ValidationError, match="exactly 1 correct answer"):
            validator.validate_content(content)

    def test_validate_only_one_answer_choice(self):
        """Test error when multiple choice has only one choice."""
        validator = SyntaxValidator()
        content = """## Question 1
[Type: multiple_choice]

Question?

*a) Only choice
"""
        with pytest.raises(ValidationError, match="at least 2 choices"):
            validator.validate_content(content)

    def test_validate_invalid_points(self):
        """Test error on invalid points value."""
        validator = SyntaxValidator()
        content = """## Question 1
[Type: multiple_choice]
[Points: not_a_number]

Question?

a) Answer
*b) Correct
"""
        with pytest.raises(ValidationError, match="not an integer"):
            validator.validate_content(content)

    def test_validate_content_with_comments(self):
        """Test that HTML comments are ignored."""
        validator = SyntaxValidator()
        content = """<!-- This is a comment -->

## Question 1
[Type: multiple_choice]

Question?

a) Answer
*b) Correct

<!-- Another comment -->
"""
        # Should not raise
        validator.validate_content(content)

    def test_validate_multiple_questions(self):
        """Test validating multiple questions."""
        validator = SyntaxValidator()
        content = """## Question 1
[Type: multiple_choice]

Q1?

a) A
*b) B

## Question 2
[Type: true_false]

Q2?

*a) True
b) False

## Question 3
[Type: multiple_choice]

Q3?

a) X
*b) Y
c) Z
"""
        # Should not raise
        validator.validate_content(content)
