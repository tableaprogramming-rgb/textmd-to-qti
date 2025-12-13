## Description

Please include a summary of the changes and related context. What problem does this solve?

Fixes # (issue)

## Type of Change

Please delete options that are not relevant:

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Documentation update
- [ ] Refactoring or code cleanup

## Testing

Please describe the tests you ran and how to reproduce them:

```bash
pytest tests/test_your_feature.py
```

## Checklist

- [ ] My code follows the code style guidelines (`black`, `ruff`, `mypy`)
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published

## Code Quality

Run before submitting:

```bash
black src/ tests/
ruff check src/ tests/
mypy src/
pytest
```

## Related Issues or Discussions

- Links to related issues or discussions
- Closes #123

## Additional Notes

Add any other context or notes here.
