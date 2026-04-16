# CONTRIBUTING.md

## Contributing to SerialCLI

Thank you for your interest in contributing to SerialCLI! This document provides guidelines and instructions for contributing.

### Code Style

#### Python Style Guide
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use 4 spaces for indentation
- Max line length: 88 characters
- Always use type hints for function parameters and returns

#### Example
```python
def connect(self, port: str, baudrate: int = 9600) -> Tuple[bool, str]:
    """
    Establish a serial connection.
    
    Args:
        port: Serial port name
        baudrate: Communication speed (default: 9600)
    
    Returns:
        Tuple of (success: bool, message: str)
    """
    # Implementation...
    return True, "Connected successfully"
```

### Project Structure

```
SerialCLI/
├── __main__.py              # Entry point
├── cli.py                   # Command-line interface
├── serial_core.py           # Serial communication
├── dev.py                   # Test framework
├── setup.py                 # Installation configuration
├── requirements.txt         # Dependencies
├── config.json              # Settings
├── dev.json                 # Test definitions
├── logo.txt                 # ASCII logo
├── README.md                # User documentation
├── QUICKSTART.md            # Getting started guide
├── ARCHITECTURE.md          # Technical architecture
└── CONTRIBUTING.md          # This file
```

### Development Setup

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/SerialCLI.git
cd SerialCLI

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install in development mode
pip install -e .

# 4. Install development dependencies
pip install pyserial

# 5. Test the installation
SerialCLI
```

### Making Changes

#### Creating a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

#### Code Organization
- One class per logical unit
- Keep methods focused and single-purpose
- Use descriptive names for variables and functions
- Add docstrings to all public methods

#### Documentation
- Update docstrings when changing function signatures
- Add inline comments for complex logic
- Update README.md if adding user-facing features
- Update ARCHITECTURE.md if modifying core structure

#### Testing
- Test your changes manually before submitting
- Ensure existing functionality still works
- Test on both Windows and Linux if possible

### Common Contributions

#### Adding a New Command

1. **Add command handler in `cli.py`**:
```python
def parse_mycommand(self, args: List[str]) -> None:
    """Parse and execute mycommand."""
    # Implementation
    
def process_command(self, user_input: str) -> None:
    # ... in process_command method:
    elif command == "mycommand":
        self.parse_mycommand(args)
```

2. **Update help text** in `print_help()` method

3. **Test the command**:
```bash
SerialCLI
SerialCLI> mycommand [args]
```

#### Adding a Test Template to dev.json

1. **Edit `dev.json`**:
```json
{
    "NAME": "NEW_TEST",
    "DESCRIPTION": "Description of the test",
    "SEQUENCE": [
        {"TX": "command1", "RX": "response1"},
        {"TX": "command2", "RX": "response2"}
    ]
}
```

2. **Test it**:
```
SerialCLI> dev devvy
SerialCLI> dev --run NEW_TEST
```

#### Improving Serial Communication

1. **Edit `serial_core.py`** - Add new methods to `SerialCommunicator`
2. **Update documentation** - Add docstrings
3. **Test thoroughly** - Test with real devices if possible

#### Enhancing Error Handling

The project uses `(bool, str)` return tuples:
```python
success, message = function_call()
if success:
    # Handle success
else:
    # Handle error: message contains error details
```

Maintain this pattern for consistency.

### Commit Guidelines

#### Commit Messages
- Use clear, descriptive messages
- Start with a verb: "Add", "Fix", "Update", "Refactor"
- Reference related issues if applicable

#### Examples
```
Add support for hardware flow control
Fix timeout handling in serial communication
Update documentation for new features
Refactor test execution logic
```

#### Commit Process
```bash
git add [files]
git commit -m "Your descriptive commit message"
git push origin feature/your-feature-name
```

### Pull Request Process

1. **Create descriptive PR title**
   - Example: "Add hardware flow control support"

2. **Provide PR description**:
   - What changes were made?
   - Why were they made?
   - How should this be tested?
   - Does it break compatibility?

3. **Include testing information**
   - How to test the changes
   - What hardware was tested with

4. **Ensure quality**
   - No syntax errors
   - Follows code style
   - All docstrings updated
   - README updated if needed

### Testing Guidelines

#### Manual Testing Checklist
```
□ Installation works (pip install -e .)
□ SerialCLI starts without errors
□ help command displays correctly
□ connect --list shows available ports
□ Connection succeeds/fails appropriately
□ Sending/receiving data works
□ Tests run correctly
□ Disconnection works
□ No memory leaks on exit
```

#### Testing Different Scenarios
- Valid and invalid port names
- Different baud rates
- Rapid connect/disconnect cycles
- Multiple test runs
- Very long command lines
- Special characters in data

### Reporting Issues

When reporting bugs:
1. **Describe the problem clearly**
2. **Include your environment**:
   - Python version
   - OS (Windows/Linux/macOS)
   - Serial device type
   - What command triggers the bug
3. **Provide step-by-step reproduction**
4. **Include error messages**:
   ```
   SerialCLI> your-command
   Error message here
   ```

### Feature Requests

When suggesting features:
1. **Describe the use case**
2. **Explain the benefit**
3. **Suggest implementation approach** (optional)
4. **Provide examples** of how it would be used

### Questions?

- Check existing issues on GitHub
- Review [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
- Check [README.md](README.md) for usage questions

### Code Review

All contributions undergo review for:
- Code quality and style
- Compatibility with existing code
- Documentation completeness
- Backward compatibility
- Security considerations

### License

By contributing to SerialCLI, you agree that your contributions will be licensed under the MIT License, the same license used by the project.

### Recognition

Contributors will be acknowledged in:
- Git commit history
- Release notes
- Contributors list (if applicable)

---

Thank you for contributing to SerialCLI! Your efforts help make this tool better for everyone. 🙏
