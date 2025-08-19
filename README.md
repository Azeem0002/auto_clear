to# AutoClear

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()

AutoClear v0.1.0 is a robust Python CLI utility for automating periodic terminal clearing tasks with configurable intervals. Built with Typer for intuitive commands and PID tracking for process management.

## Features

- 🚀 Start/stop automated terminal clearing
- ⏱️ Customizable time intervals (minutes)
- 🔒 PID file locking prevents multiple instances
- 🛠️ Graceful error handling with user prompts
- 📊 Real-time status monitoring

## Installation

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Setup

```bash
# Clone repository
git clone https://github.com/Azeem0002/auto_clear
cd auto_clear

# Create virtual environment
python -m venv .venv

# Activate environment
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate.bat   # Windows

# Install dependencies
uv pip install .
uv pip install -e .  # For development
```

### Usage

```bash
# Start with 10-minute interval (default)
autoclear start or autoclear 

# Start with custom interval
autoclear start -t 5  # 5 minutes

# Check status
autoclear status

# Stop process
autoclear stop
```

### Project Structure

```plaintext
auto_clear/
├── src/
│   ├── controller.py    # CLI command handlers
│   └── autoclear.py     # Core clearing logic
├── tests/               # Unit tests
├── pyproject.toml       # Build configuration
└── README.md
```

### Dev

```bash
# Install development dependencies
uv pip install -e "[dev]"

# Run tests
pytest tests/

# Formatting $ Linting
ruff check .
```

### Common Issues

```bash
# Ensure virtualenv is activated
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate.bat   # Windows

# Reinstall package
pip install --force-reinstall .
```
