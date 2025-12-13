"""Tests for Pydantic question models."""

import pytest
from pydantic import ValidationError

from text_to_qti.parser.question_models import (
    AnswerChoice,
    Question,
    QuestionType,
    Quiz,
    QuizMetadata,
)


class TestAnswerChoice:
    """Tests for AnswerChoice model."""

    def test_valid_choice(self):
        """Test creating a valid answer choice."""
        choice = AnswerChoice(letter="a", text="Answer text", is_correct=False)
        assert choice.letter == "a"
        assert choice.text == "Answer text"
        assert not choice.is_correct

    def test_correct_choice(self):
        """Test creating a correct answer choice."""
        choice = AnswerChoice(letter="b", text="Correct answer", is_correct=True)
        assert choice.is_correct

    def test_invalid_letter_uppercase(self):
        """Test that uppercase letters are rejected."""
        with pytest.raises(ValidationError):
            AnswerChoice(letter="A", text="Answer", is_correct=False)

    def test_invalid_letter_multiple(self):
        """Test that multiple characters are rejected."""
        with pytest.raises(ValidationError):
            AnswerChoice(letter="ab", text="Answer", is_correct=False)

    def test_empty_text(self):
        """Test that empty text is rejected."""
        with pytest.raises(ValidationError):
            AnswerChoice(letter="a", text="", is_correct=False)

    def test_whitespace_only_text(self):
        """Test that whitespace-only text is rejected."""
        with pytest.raises(ValidationError):
            AnswerChoice(letter="a", text="   ", is_correct=False)


class TestQuestion:
    """Tests for Question model."""

    def test_multiple_choice_question(self):
        """Test creating a valid multiple choice question."""
        question = Question(
            type=QuestionType.MULTIPLE_CHOICE,
            text="What is 2+2?",
            choices=[
                AnswerChoice(letter="a", text="3", is_correct=False),
                AnswerChoice(letter="b", text="4", is_correct=True),
                AnswerChoice(letter="c", text="5", is_correct=False),
            ],
        )
        assert question.type == QuestionType.MULTIPLE_CHOICE
        assert len(question.choices) == 3

    def test_true_false_question(self):
        """Test creating a valid true/false question."""
        question = Question(
            type=QuestionType.TRUE_FALSE,
            text="The sky is blue.",
            choices=[
                AnswerChoice(letter="a", text="True", is_correct=True),
                AnswerChoice(letter="b", text="False", is_correct=False),
            ],
        )
        assert question.type == QuestionType.TRUE_FALSE

    def test_question_with_feedback(self):
        """Test question with feedback."""
        question = Question(
            type=QuestionType.MULTIPLE_CHOICE,
            text="What color is the sky?",
            choices=[
                AnswerChoice(letter="a", text="Blue", is_correct=True),
                AnswerChoice(letter="b", text="Red", is_correct=False),
            ],
            feedback="The sky appears blue due to Rayleigh scattering.",
        )
        assert question.feedback is not None

    def test_empty_question_text(self):
        """Test that empty question text is rejected."""
        with pytest.raises(ValidationError):
            Question(
                type=QuestionType.MULTIPLE_CHOICE,
                text="",
                choices=[
                    AnswerChoice(letter="a", text="Answer", is_correct=True),
                    AnswerChoice(letter="b", text="Other", is_correct=False),
                ],
            )

    def test_no_correct_answer(self):
        """Test that questions without correct answers are rejected."""
        with pytest.raises(ValidationError):
            Question(
                type=QuestionType.MULTIPLE_CHOICE,
                text="Question?",
                choices=[
                    AnswerChoice(letter="a", text="Answer 1", is_correct=False),
                    AnswerChoice(letter="b", text="Answer 2", is_correct=False),
                ],
            )

    def test_non_sequential_letters(self):
        """Test that non-sequential letters are rejected."""
        with pytest.raises(ValidationError):
            Question(
                type=QuestionType.MULTIPLE_CHOICE,
                text="Question?",
                choices=[
                    AnswerChoice(letter="a", text="Answer 1", is_correct=True),
                    AnswerChoice(letter="c", text="Answer 2", is_correct=False),
                ],
            )

    def test_true_false_wrong_count(self):
        """Test that true/false with wrong number of choices is rejected."""
        with pytest.raises(ValidationError):
            Question(
                type=QuestionType.TRUE_FALSE,
                text="Is this true?",
                choices=[
                    AnswerChoice(letter="a", text="True", is_correct=True),
                    AnswerChoice(letter="b", text="False", is_correct=False),
                    AnswerChoice(letter="c", text="Maybe", is_correct=False),
                ],
            )

    def test_multiple_choice_multiple_correct(self):
        """Test that multiple choice with multiple correct answers is rejected."""
        with pytest.raises(ValidationError):
            Question(
                type=QuestionType.MULTIPLE_CHOICE,
                text="Question?",
                choices=[
                    AnswerChoice(letter="a", text="Answer 1", is_correct=True),
                    AnswerChoice(letter="b", text="Answer 2", is_correct=True),
                ],
            )


class TestQuizMetadata:
    """Tests for QuizMetadata model."""

    def test_valid_metadata(self):
        """Test creating valid quiz metadata."""
        metadata = QuizMetadata(title="My Quiz")
        assert metadata.title == "My Quiz"
        assert metadata.points_per_question == 1
        assert not metadata.shuffle_answers

    def test_with_description(self):
        """Test metadata with description."""
        metadata = QuizMetadata(
            title="My Quiz",
            description="This is a quiz",
            points_per_question=2,
            shuffle_answers=True,
        )
        assert metadata.description == "This is a quiz"
        assert metadata.points_per_question == 2
        assert metadata.shuffle_answers

    def test_empty_title(self):
        """Test that empty title is rejected."""
        with pytest.raises(ValidationError):
            QuizMetadata(title="")


class TestQuiz:
    """Tests for Quiz model."""

    def test_valid_quiz(self):
        """Test creating a valid quiz."""
        metadata = QuizMetadata(title="Quiz")
        question = Question(
            type=QuestionType.MULTIPLE_CHOICE,
            text="Question?",
            choices=[
                AnswerChoice(letter="a", text="Answer", is_correct=True),
                AnswerChoice(letter="b", text="Other", is_correct=False),
            ],
        )
        quiz = Quiz(metadata=metadata, questions=[question])
        assert len(quiz.questions) == 1

    def test_total_points(self):
        """Test calculating total quiz points."""
        metadata = QuizMetadata(title="Quiz")
        q1 = Question(
            type=QuestionType.MULTIPLE_CHOICE,
            text="Q1?",
            choices=[
                AnswerChoice(letter="a", text="A1", is_correct=True),
                AnswerChoice(letter="b", text="B1", is_correct=False),
            ],
            points=2,
        )
        q2 = Question(
            type=QuestionType.TRUE_FALSE,
            text="Q2?",
            choices=[
                AnswerChoice(letter="a", text="True", is_correct=True),
                AnswerChoice(letter="b", text="False", is_correct=False),
            ],
            points=3,
        )
        quiz = Quiz(metadata=metadata, questions=[q1, q2])
        assert quiz.get_total_points() == 5

    def test_no_questions(self):
        """Test that quiz without questions is rejected."""
        metadata = QuizMetadata(title="Quiz")
        with pytest.raises(ValidationError):
            Quiz(metadata=metadata, questions=[])

    def test_duplicate_ids(self):
        """Test that duplicate question IDs are rejected."""
        metadata = QuizMetadata(title="Quiz")
        q1 = Question(
            id="q1",
            type=QuestionType.MULTIPLE_CHOICE,
            text="Q1?",
            choices=[
                AnswerChoice(letter="a", text="A1", is_correct=True),
                AnswerChoice(letter="b", text="B1", is_correct=False),
            ],
        )
        q2 = Question(
            id="q1",
            type=QuestionType.TRUE_FALSE,
            text="Q2?",
            choices=[
                AnswerChoice(letter="a", text="True", is_correct=True),
                AnswerChoice(letter="b", text="False", is_correct=False),
            ],
        )
        with pytest.raises(ValidationError):
            Quiz(metadata=metadata, questions=[q1, q2])
