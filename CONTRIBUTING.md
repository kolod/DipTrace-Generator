# Contributing to DipTrace Generator

First off, thank you for considering contributing to DipTrace Generator! We welcome contributions from everyone.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)

## Code of Conduct

This project and everyone participating in it is governed by basic principles of respect and professionalism. By participating, you are expected to uphold these standards.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:

   ```bash
   git clone https://github.com/YOUR-USERNAME/DipTrace-Generator.git
   cd DipTrace-Generator
   ```

3. **Create a branch** for your changes:

   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Prerequisites

- Python 3.9 or higher
- [Poetry](https://python-poetry.org/) for dependency management

### Installation

1. Install dependencies:

   ```bash
   poetry install
   ```

2. Activate the virtual environment:

   ```bash
   poetry shell
   ```

### Running Tests

Run all tests with coverage:

```bash
poetry run pytest tests --cov=DipTraceGenerator --cov-report=term --cov-report=term-missing
```

Run specific test file:

```bash
poetry run pytest tests/test_Pattern_Library.py -v
```

Run tests matching a pattern:

```bash
poetry run pytest tests/ -k "Pattern" -v
```

### Building Examples

Generate example libraries:

```bash
poetry run examples
```

### Building the Package

```bash
poetry build
```

## Coding Standards

This project follows **Google Python Style Guide** with type hints in function signatures only.

### Code Style Guidelines

#### 1. Docstrings (Google Style)

Use Google-style docstrings with types **only in function signatures**:

```python
def from_xml(cls, element: etree._Element, units: Units) -> 'Pattern':
    """
    Parse Pattern from XML element.
    
    Reads values from the file in the specified units and converts them 
    to internal MM representation.
    
    Args:
        element: XML element representing the Pattern.
        units: Units used in the source file (MM, INCH, or MIL).
        
    Returns:
        Pattern instance with all dimensions in MM.
        
    Raises:
        ValueError: If required attributes are missing.
    """
    # Implementation here
    pass
```

**Key Points:**

- Types are in the function signature, **not** in the docstring
- Use clear, descriptive text in Args/Returns sections
- Include Raises section when exceptions can be raised
- Keep docstrings concise but complete

#### 2. Type Hints

Always use type hints in function signatures:

```python
from typing import Union, Optional
from pathlib import Path

def to_file(
    self, 
    filename: Union[Path, str], 
    units: Units = Units.MM,
    encoding: str = "utf-8", 
    pretty_print: bool = True
) -> None:
    """Save Library to XML file."""
    pass
```

#### 3. Imports

Organize imports in three groups:

1. Standard library imports
2. Third-party imports
3. Local application imports

```python
# Standard library
from typing import Union
from pathlib import Path

# Third-party
from lxml import etree

# Local
from ..Units import Units
from .Pattern import Pattern
```

#### 4. Code Formatting

- **Indentation**: 4 spaces (no tabs)
- **Line length**: Maximum 120 characters (soft limit)
- **Naming conventions**:
  - Classes: `PascalCase` (e.g., `PatternLibrary`)
  - Functions/methods: `snake_case` (e.g., `from_xml`)
  - Constants: `UPPER_SNAKE_CASE` (e.g., `DEFAULT_VERSION`)
  - Private members: Prefix with `_` (e.g., `_internal_method`)

#### 5. Class Structure

Use dataclasses where appropriate:

```python
from dataclasses import dataclass, field

@dataclass
class Library:
    """
    Represents a DipTrace Pattern Library file.
    
    Attributes:
        type: Library type identifier.
        name: Library name displayed in the UI.
        patterns: List of patterns in the library.
    """
    
    type: str = "DipTrace-PatternLibrary"
    name: str = ""
    patterns: list[Pattern] = field(default_factory=list)
```

#### 6. Error Handling

Be explicit about error conditions:

```python
def load_file(filename: str) -> Library:
    """
    Load library from file.
    
    Args:
        filename: Path to the library file.
        
    Returns:
        Loaded Library instance.
        
    Raises:
        TypeError: If filename is empty or invalid.
        FileNotFoundError: If file doesn't exist.
    """
    if not filename:
        raise TypeError("Filename must be a non-empty string")
    
    if not Path(filename).exists():
        raise FileNotFoundError(f"File not found: {filename}")
    
    # Load file...
```

## Testing Guidelines

### Test Requirements

- **All new code must have tests**
- **Aim for 100% code coverage**
- **Tests should be clear and maintainable**

### Test Structure

Use `unittest` framework:

```python
from unittest import TestCase, main

class TestPattern(TestCase):
    """Test the Pattern class."""
    
    def test_create_pattern_defaults(self):
        """Test creating a Pattern with default values."""
        pattern = Pattern()
        self.assertEqual(pattern.name, "")
        self.assertEqual(pattern.mounting, None)
    
    def test_pattern_from_xml_basic(self):
        """Test parsing Pattern from basic XML."""
        xml_string = '''<Pattern ID="0" Name="Test" RefDes="U"/>'''
        element = etree.fromstring(xml_string)
        pattern = Pattern.from_xml(element, Units.MM)
        
        self.assertEqual(pattern.id, 0)
        self.assertEqual(pattern.name, "Test")
        self.assertEqual(pattern.ref_des, "U")

if __name__ == '__main__':
    main()
```

### Test Naming

- Test files: `test_<module_name>.py`
- Test classes: `Test<ClassName>`
- Test methods: `test_<what_it_tests>`

### Coverage Requirements

Check coverage after adding tests:

```bash
poetry run pytest tests/test_your_module.py --cov=DipTraceGenerator.YourModule --cov-report=term-missing
```

Strive for 100% coverage. Uncovered lines should have a good reason.

## Submitting Changes

### Commit Messages

Write clear, descriptive commit messages:

```text
Add unit conversion support to Pattern.Library

- Implement automatic unit detection in from_xml()
- Add units parameter to to_xml() and to_file()
- Update all tests for new unit conversion behavior
- Achieve 100% test coverage for Library class

Fixes #123
```

**Format:**

- **First line**: Brief summary (50 chars or less)
- **Body**: Detailed explanation of changes
- **Footer**: Reference issues/PRs

### Signed Commits

If you're using GPG signing and have issues in devcontainer, see the [README](README.md#signed-commit) for troubleshooting.

### Pull Request Process

1. **Update your branch** with the latest changes from main:

```bash
git fetch upstream
git rebase upstream/main
```

1. **Run all tests** and ensure they pass:

```bash
poetry run pytest tests --cov=DipTraceGenerator
```

1. **Push your changes**:

```bash
git push origin feature/your-feature-name
```

1. **Open a Pull Request** on GitHub with:

- Clear description of changes
- Link to related issues
- Screenshots (if applicable)
- Test results/coverage report

1. **Address review feedback** promptly and professionally

### PR Requirements

- [ ] All tests pass
- [ ] Code coverage is maintained or improved
- [ ] Code follows project style guidelines
- [ ] Documentation is updated (if applicable)
- [ ] Commit messages are clear and descriptive

## Reporting Bugs

### Before Submitting a Bug Report

- **Check existing issues** to avoid duplicates
- **Verify the bug** in the latest version
- **Collect information** about your environment

### Bug Report Template

```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Load library with '...'
2. Call method '...'
3. See error

**Expected behavior**
What you expected to happen.

**Actual behavior**
What actually happened.

**Environment:**
 - OS: [e.g. Windows 11, Ubuntu 22.04]
 - Python version: [e.g. 3.11.5]
 - Package version: [e.g. 0.1.1]

**Additional context**
Stack traces, error messages, or screenshots.
```

## Suggesting Enhancements

### Enhancement Proposal Template

```markdown
**Is your feature request related to a problem?**
A clear description of the problem.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
Other approaches you've thought about.

**Additional context**
Any other context, mockups, or examples.
```

## Development Tips

### Project Structure

```text
DipTraceGenerator/
├── Pattern/            # Pattern library classes
│   ├── Library.py      # Library container
│   ├── Pattern.py      # Pattern footprints
│   ├── PadStyle.py     # Pad style definitions
│   └── ...
├── Component/          # Component library classes (future)
├── Units.py           # Unit conversion utilities
└── ...

tests/
├── test_Pattern_Library.py
├── test_Pattern_Pattern.py
└── samples/           # Sample files for testing
```

### Working with XML

The project uses `lxml` for XML processing:

```python
from lxml import etree
from ..xmltools import E

# Creating elements
element = E("Pattern", {"ID": "0", "Name": "Test"})

# Parsing
tree = etree.parse(filename)
root = tree.getroot()

# Writing
tree.write(filename, encoding="utf-8", xml_declaration=True, pretty_print=True)
```

### Unit Conversion

All dimensions are stored internally in millimeters (MM):

```python
from ..Units import Units, convert_units

# Convert from file units to internal MM
width_mm = convert_units(width_value, from_units=Units.INCH, to_units=Units.MM)

# Convert from internal MM to output units
width_inch = convert_units(width_mm, from_units=Units.MM, to_units=Units.INCH)
```

## Questions?

If you have questions about contributing:

1. Check existing documentation
2. Look for similar issues/PRs
3. Open a new issue with the `question` label

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Glory to Ukraine! 🇺🇦
