"""Pytest configuration and fixtures."""

import pytest
from pathlib import Path


@pytest.fixture
def fixtures_dir() -> Path:
    """Return path to fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def simple_mc_file(fixtures_dir: Path) -> Path:
    """Return path to simple multiple choice fixture."""
    return fixtures_dir / "simple_mc.txt"


@pytest.fixture
def simple_tf_file(fixtures_dir: Path) -> Path:
    """Return path to simple true/false fixture."""
    return fixtures_dir / "simple_tf.txt"


@pytest.fixture
def mixed_questions_file(fixtures_dir: Path) -> Path:
    """Return path to mixed questions fixture."""
    return fixtures_dir / "mixed_questions.txt"
