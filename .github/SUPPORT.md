# Support

Need help with text-to-qti? Here are the best ways to get support:

## Documentation

Start with our comprehensive documentation:

- **[QUICK_START.md](/QUICK_START.md)** - Get up and running in 5 minutes
- **[QUIZ_SYNTAX_GUIDE.md](/QUIZ_SYNTAX_GUIDE.md)** - Detailed syntax reference
- **[README.md](/README.md)** - Full project documentation
- **[TEMPLATE.txt](/TEMPLATE.txt)** - Ready-to-use quiz template

## Asking Questions

### GitHub Discussions
For general questions and discussions, use [GitHub Discussions](https://github.com/tableaprogramming-rgb/textmd-to-qti/discussions).

Good topics for discussions:
- How to... questions
- Best practices
- Feedback and suggestions
- Feature discussions

### GitHub Issues
For bug reports and specific problems, use [GitHub Issues](https://github.com/tableaprogramming-rgb/textmd-to-qti/issues).

Please include:
- Detailed description of the problem
- Steps to reproduce
- Your quiz file (with sensitive content removed)
- Error message and traceback
- Your environment (OS, Python version, installation method)

## Email Contact

For security concerns or private inquiries, email **tableaprogramming@gmail.com**.

## Troubleshooting

### Common Issues

**"No questions found" error**
- Ensure your quiz file has questions starting with `## Question 1`, `## Question 2`, etc.
- Check that you have proper YAML front matter if using metadata
- See [QUIZ_SYNTAX_GUIDE.md](/QUIZ_SYNTAX_GUIDE.md) for correct format

**"Invalid question type" error**
- Question type must be either `multiple_choice` or `true_false`
- Use format: `[Type: multiple_choice]`
- See [QUICK_START.md](/QUICK_START.md) for examples

**Canvas import fails**
- Verify the generated ZIP file is not corrupted
- Check that you're using Canvas with QTI 1.2 support
- Try re-generating and re-uploading the package

**File encoding issues**
- Ensure your quiz file is UTF-8 encoded
- On Windows, save file as UTF-8 in your text editor
- Never use ANSI or other encodings

## Contributing

Want to help improve text-to-qti? See [CONTRIBUTING.md](/CONTRIBUTING.md) for guidelines on:
- Setting up development environment
- Submitting pull requests
- Code style requirements
- Running tests locally

## Security Issues

If you discover a security vulnerability, please do NOT open a public issue. Instead, see [SECURITY.md](/SECURITY.md) for responsible disclosure guidelines.

---

We're here to help! Don't hesitate to ask questions or report issues.
