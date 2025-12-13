"""Tests for QTI generator."""

import tempfile
import zipfile
from pathlib import Path

import pytest

from text_to_qti.parser.markdown_parser import MarkdownParser
from text_to_qti.qti.generator import QTIGenerator


class TestQTIGenerator:
    """Tests for QTIGenerator class."""

    def test_generate_simple_quiz(self, simple_mc_file: Path):
        """Test generating QTI from simple quiz."""
        parser = MarkdownParser()
        quiz = parser.parse_file(str(simple_mc_file))

        generator = QTIGenerator(quiz)

        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as f:
            output_path = f.name

        try:
            result = generator.generate(output_path)
            assert result.exists()
            assert result.suffix == ".zip"
        finally:
            Path(output_path).unlink(missing_ok=True)

    def test_zip_structure(self, mixed_questions_file: Path):
        """Test ZIP package structure (Canvas compatible format)."""
        parser = MarkdownParser()
        quiz = parser.parse_file(str(mixed_questions_file))

        generator = QTIGenerator(quiz)

        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as f:
            output_path = f.name

        try:
            generator.generate(output_path)

            with zipfile.ZipFile(output_path, "r") as zf:
                names = zf.namelist()

                # Check required files (Canvas format)
                assert "imsmanifest.xml" in names
                assert "ASSESSMENT_001/ASSESSMENT_001.xml" in names
                assert "ASSESSMENT_001/assessment_meta.xml" in names
        finally:
            Path(output_path).unlink(missing_ok=True)

    def test_manifest_content(self, simple_mc_file: Path):
        """Test manifest contains proper references (Canvas format)."""
        parser = MarkdownParser()
        quiz = parser.parse_file(str(simple_mc_file))

        generator = QTIGenerator(quiz)

        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as f:
            output_path = f.name

        try:
            generator.generate(output_path)

            with zipfile.ZipFile(output_path, "r") as zf:
                manifest = zf.read("imsmanifest.xml").decode("utf-8")

                # Check manifest structure (Canvas format)
                assert "ASSESSMENT_001" in manifest
                assert "imsqti_xmlv1p2" in manifest
                assert "ASSESSMENT_001/ASSESSMENT_001.xml" in manifest
                assert "assessment_meta.xml" in manifest
        finally:
            Path(output_path).unlink(missing_ok=True)

    def test_item_has_correct_answer(self, simple_mc_file: Path):
        """Test that item XML marks correct answer (embedded in assessment)."""
        parser = MarkdownParser()
        quiz = parser.parse_file(str(simple_mc_file))

        generator = QTIGenerator(quiz)

        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as f:
            output_path = f.name

        try:
            generator.generate(output_path)

            with zipfile.ZipFile(output_path, "r") as zf:
                # Get assessment file (items are now embedded)
                assessment_content = zf.read(
                    "ASSESSMENT_001/ASSESSMENT_001.xml"
                ).decode("utf-8")

                # Check for correct answer and response processing
                assert "CHOICE_C" in assessment_content  # Paris is C
                assert "respcondition" in assessment_content
                assert "setvar" in assessment_content
        finally:
            Path(output_path).unlink(missing_ok=True)

    def test_true_false_question(self, simple_tf_file: Path):
        """Test true/false question generation."""
        parser = MarkdownParser()
        quiz = parser.parse_file(str(simple_tf_file))

        generator = QTIGenerator(quiz)

        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as f:
            output_path = f.name

        try:
            generator.generate(output_path)

            with zipfile.ZipFile(output_path, "r") as zf:
                # Get assessment file (items are embedded)
                assessment_content = zf.read(
                    "ASSESSMENT_001/ASSESSMENT_001.xml"
                ).decode("utf-8")

                # Check for true/false specific marker
                assert "true_false_question" in assessment_content
        finally:
            Path(output_path).unlink(missing_ok=True)

    def test_assessment_has_items(self, mixed_questions_file: Path):
        """Test assessment embeds all items."""
        parser = MarkdownParser()
        quiz = parser.parse_file(str(mixed_questions_file))

        generator = QTIGenerator(quiz)

        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as f:
            output_path = f.name

        try:
            generator.generate(output_path)

            with zipfile.ZipFile(output_path, "r") as zf:
                assessment = zf.read("ASSESSMENT_001/ASSESSMENT_001.xml").decode(
                    "utf-8"
                )

                # Check that assessment has section with embedded items
                assert "<section" in assessment
                assert "<item ident=" in assessment
                # Should have 3 items embedded (count opening item tags)
                assert assessment.count('<item ident="') == 3
        finally:
            Path(output_path).unlink(missing_ok=True)

    def test_multiple_points(self, mixed_questions_file: Path):
        """Test that custom points are included in metadata."""
        parser = MarkdownParser()
        quiz = parser.parse_file(str(mixed_questions_file))

        generator = QTIGenerator(quiz)

        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as f:
            output_path = f.name

        try:
            generator.generate(output_path)

            with zipfile.ZipFile(output_path, "r") as zf:
                # Assessment file contains all items
                assessment_content = zf.read(
                    "ASSESSMENT_001/ASSESSMENT_001.xml"
                ).decode("utf-8")

                # Third question has 2 points (stored as float 2.0)
                assert "<fieldentry>2.0</fieldentry>" in assessment_content
        finally:
            Path(output_path).unlink(missing_ok=True)
