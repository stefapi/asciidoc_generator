# Contributing to AsciiDoc Generator

Thank you for your interest in contributing to the AsciiDoc Generator project! This document provides guidelines for contributing to the project.

## Getting Started

### Prerequisites

Before contributing, ensure you have the following dependencies installed:

- Python 3.7 or higher
- LibreOffice
- Pandoc with Lua support
- Asciidoctor with required extensions (see README.asc for details)

### Setting up the Development Environment

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd asciidoc_generator
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Test the installation:
   ```bash
   make all
   ```

## How to Contribute

### Reporting Issues

- Use the GitHub issue tracker to report bugs or request features
- Provide detailed information about the issue, including:
  - Steps to reproduce
  - Expected behavior
  - Actual behavior
  - Environment details (OS, Python version, etc.)

### Submitting Changes

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test your changes thoroughly
5. Commit your changes with clear, descriptive messages
6. Push to your fork: `git push origin feature-name`
7. Submit a pull request

### Code Style Guidelines

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Ensure scripts are executable and have proper shebang lines
- Test your changes with the provided sample files

### Testing

- Test your changes with the sample.asc file
- Verify that all output formats (ODT, DOCX, PDF) are generated correctly
- Test template generation and modification workflows
- Ensure LibreOffice macros work correctly

### Documentation

- Update README.asc if you add new features or change existing functionality
- Update template/README.asc for template-related changes
- Add comments to complex code sections
- Update this CONTRIBUTING.md file if you change the contribution process

## Project Structure

- `scripts/` - Main processing scripts
- `template/` - Document templates and template generation tools
- `medias/` - Media files directory
- `sample.asc` - Sample AsciiDoc file for testing

## Questions?

If you have questions about contributing, please open an issue or contact the maintainers.

Thank you for contributing!
