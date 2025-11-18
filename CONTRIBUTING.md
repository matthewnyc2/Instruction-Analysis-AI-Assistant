# Contributing to Instruction Analysis AI Assistant

Thank you for your interest in contributing to the Instruction Analysis AI Assistant!

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/matthewnyc2/Instruction-Analysis-AI-Assistant.git
   cd Instruction-Analysis-AI-Assistant
   ```

2. Install the package in development mode:
   ```bash
   make install
   # or
   pip install -e .
   ```

## Running Tests

We have comprehensive test coverage with 52+ tests. To run tests:

```bash
# Run all tests
make test

# Run tests with verbose output
make test-verbose

# Or use unittest directly
python -m unittest discover -s tests -v
```

## Code Quality

Before submitting changes:

```bash
# Check Python syntax
make lint

# Clean build artifacts
make clean
```

## Project Structure

```
Instruction-Analysis-AI-Assistant/
├── run_analysis.py           # CLI entry point
├── tools/
│   └── parsers/              # Analysis tools
│       ├── markdown_parser.py
│       ├── dependency_analyzer.py
│       └── pseudocode_validator.py
├── prompts/                  # AI prompt templates
├── examples/                 # Example inputs/outputs
└── tests/                    # Test suite
```

## Adding New Features

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Write tests first** (TDD approach):
   - Add unit tests in `tests/test_*.py`
   - Ensure all tests pass

3. **Implement your feature**:
   - Follow existing code style
   - Add docstrings to functions and classes
   - Use type hints where appropriate

4. **Test your changes**:
   ```bash
   make test
   make lint
   ```

5. **Submit a pull request**:
   - Describe your changes
   - Reference any related issues
   - Ensure CI tests pass

## Writing Tests

We use Python's built-in `unittest` framework:

```python
import unittest

class TestNewFeature(unittest.TestCase):
    def test_something(self):
        # Arrange
        input_data = "test"

        # Act
        result = your_function(input_data)

        # Assert
        self.assertEqual(result, expected_output)
```

## Code Style Guidelines

- Use clear, descriptive variable and function names
- Add docstrings to all public functions and classes
- Keep functions focused and concise
- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values

## Adding New Prompts

When adding new prompt templates to `prompts/`:

1. Create a new directory for the phase: `prompts/your-phase/`
2. Add a markdown file with clear instructions
3. Include examples in the prompt
4. Document the expected output format
5. Add example outputs to `examples/outputs/`

## CI/CD

We use GitHub Actions for continuous integration:

- Tests run on Python 3.8, 3.9, 3.10, 3.11, 3.12
- Tests run on Ubuntu, macOS, and Windows
- All tests must pass before merging

## Questions?

If you have questions or need help:

- Open an issue on GitHub
- Check existing issues for similar questions
- Review the README.md for project documentation

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
