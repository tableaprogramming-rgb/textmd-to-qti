# Publishing Guide for Maintainers

This document outlines the process for publishing text-to-qti to PyPI and creating GitHub releases.

## Prerequisites

You'll need:
- Admin access to the GitHub repository
- PyPI account with authorization to publish `text-to-qti`
- GitHub Actions configured with `PYPI_API_TOKEN` secret

## Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., 1.0.0)
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes only

Examples:
- `0.1.0` → Initial release
- `0.2.0` → Add fill-in-the-blank question type
- `0.2.1` → Fix parsing bug in feedback text
- `1.0.0` → First stable release

## Release Checklist

### 1. Prepare the Release

- [ ] All tests pass locally: `pytest`
- [ ] All code quality checks pass:
  ```bash
  black src/ tests/
  ruff check src/ tests/
  mypy src/
  ```
- [ ] No uncommitted changes: `git status`
- [ ] You're on the `main` branch: `git branch`

### 2. Update Version Number

Edit `pyproject.toml`:

```toml
[project]
version = "0.2.0"  # Update this
```

### 3. Update CHANGELOG.md

Add an entry under the appropriate version:

```markdown
## [0.2.0] - 2025-01-15

### Added
- Fill-in-the-blank question type support
- Custom question shuffling within quiz

### Fixed
- Parser bug with multiline feedback text

### Changed
- Improved error messages for validation failures
```

Keep the format consistent with [Keep a Changelog](https://keepachangelog.com/).

### 4. Commit and Push

```bash
git add pyproject.toml CHANGELOG.md
git commit -m "Release v0.2.0"
git push origin main
```

### 5. Create GitHub Release (Automatic via GitHub Actions)

### Option A: Automated Release (Recommended)

GitHub Actions automatically publishes to PyPI when you create a release tag.

```bash
# Create and push the tag
git tag v0.2.0
git push origin v0.2.0
```

Then:
1. Go to GitHub repository
2. Click "Releases"
3. Click "Create a release"
4. Select the tag you just created
5. Add release notes (copy from CHANGELOG.md)
6. Click "Publish release"

GitHub Actions will automatically:
- Run full test suite
- Build the package
- Publish to PyPI

### Option B: Manual Release

If you prefer manual control:

```bash
# Build the package
python -m build

# Upload to PyPI
python -m twine upload dist/
```

## Post-Release

### Verify Package on PyPI

1. Visit https://pypi.org/project/text-to-qti/
2. Verify the new version appears
3. Test installation:
   ```bash
   pip install --upgrade text-to-qti
   text-to-qti --version
   ```

### Update Installation Guide (if needed)

If there are breaking changes or new installation steps, update:
- README.md Installation section
- Documentation with new features

### Create Announcement

Consider announcing on:
- GitHub Discussions
- Project documentation
- Community channels (if applicable)

## Rollback Procedure

If a critical bug is found in a released version:

### 1. Yank the Version from PyPI

```bash
python -m twine yank text-to-qti-0.2.0 -r pypi
```

This marks the version as unsafe without removing it.

### 2. Release a Patch Version

```bash
# Fix the bug
# Commit: git commit -m "Fix critical bug"
# Update version: 0.2.0 → 0.2.1
# Update CHANGELOG.md
git tag v0.2.1
git push origin v0.2.1
```

### 3. Announce the Fix

Notify users to upgrade to the patched version.

## Maintenance Schedule

### Regular Tasks

- **Weekly**: Monitor GitHub issues and discussions
- **Bi-weekly**: Review pull requests
- **Monthly**: Plan next release based on accumulated features/fixes
- **Quarterly**: Review roadmap and community feedback

### When to Release

Release a new version when:
- New features are ready for testing
- Critical bugs are fixed
- Documentation is updated
- Test coverage is maintained

Don't release just for the sake of it. Batching changes leads to fewer maintenance overhead.

## Long-Term Support (LTS)

Current plan: No LTS versions yet.

When we reach v2.0.0, we may consider:
- LTS versions (e.g., v2.4 LTS)
- Extended security updates for LTS
- Clear deprecation policy

## CI/CD Pipeline

The `.github/workflows/publish.yml` workflow:

```yaml
name: Publish to PyPI
on:
  release:
    types: [created]
```

This automatically:
1. Checks out the code
2. Runs full test suite
3. Builds distribution package
4. Publishes to PyPI using `PYPI_API_TOKEN`

### Setting Up PyPI Token

1. Create PyPI account at https://pypi.org
2. Generate API token in account settings
3. Add to GitHub repository secrets:
   - Name: `PYPI_API_TOKEN`
   - Value: Your PyPI API token
4. GitHub Actions will use it automatically

## Troubleshooting

### Build Fails

Check that:
- `pyproject.toml` is valid (run `pip install -e .` locally)
- All dependencies are specified
- Tests pass locally first

### Upload Fails

Check:
- PyPI token is valid
- Token has upload permissions for `text-to-qti`
- Network connectivity

### Version Already Exists

If you try to upload a version that already exists on PyPI:
1. Yank the old version (see Rollback Procedure)
2. Or increment patch version and re-release

## Documentation

- See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines
- See [README.md](README.md) for user documentation
- See [CHANGELOG.md](CHANGELOG.md) for version history

## Questions?

- Check existing releases: https://github.com/tableaprogramming-rgb/textmd-to-qti/releases
- Review PyPI docs: https://packaging.python.org/tutorials/packaging-projects/
- Ask in GitHub Discussions
