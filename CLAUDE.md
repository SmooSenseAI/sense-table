# SenseTable - Claude Code Documentation

## Overview
SenseTable is a web-based application for exploring and analyzing large-scale multi-modal tabular data.
It provides a web interface for working with CSV, Parquet, and other data formats with SQL querying capabilities.

## Architecture
- **CLI Entry Point**: `sense_table/cli.py` - Command-line interface with automatic port selection and browser opening
- **Main App**: `sense_table/app.py` - Core SenseTableApp Flask application
- **Settings**: `sense_table/settings.py` - Configuration management. This file is compiled from source file in a different repo.
- **Frontend**: `sense_table/statics` - Bundled next.js files.
- **Database**: `duckdb` based on file systems

## Development Commands

### Installation
Always use `uv` for dependency management.
```bash
# Install dependencies (example)
uv add flask
```

### Running the Application
```bash
# Start the web interface (auto-selects port, opens browser)
sense

# Show version
sense --version
```

### Testing
```bash
make test
```

### Linting/Type Checking
```bash
# Run linting (check only)
uv run ruff check

# Run linting with auto-fix
uv run ruff check --fix

# Run formatting (check only)
uv run ruff format --check

# Run formatting (apply changes)
uv run ruff format

# Run type checking
uv run mypy sense_table

# Run all checks
uv run ruff check && uv run ruff format --check && uv run mypy sense_table
```

### Building
```bash
make build
```

## Key Features
- Multi-modal data support (CSV, Parquet, etc.)
- SQL querying capabilities
- Folder browser with configurable root directory

## File Structure
```
sense_table/
├── cli.py              # CLI entry point and main function
├── app.py              # Flask application core
├── settings.py         # Configuration settings
└── ...
pyproject.toml          # Python project configuration
uv.lock                 # Dependency lock file
```

## Recent Changes
- Modified CLI to auto-select available ports
- Added automatic browser opening with threading
- Removed manual port selection to keep CLI simple

---

## Information Needed from Developer

### Build & Test Commands
- What commands should be run for testing?
- What commands should be run for linting/type checking?
- What is the standard build process?
- Are there any pre-commit hooks or CI requirements?

### Development Environment
- Are there any special environment variables or configuration files needed?
- Any specific Python version requirements?
- Are there database migrations or setup steps required?



