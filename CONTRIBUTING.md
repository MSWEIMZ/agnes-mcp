# Contributing to Agnes MCP

Thanks for your interest in contributing! 🎉

## Getting Started

```bash
# Clone the repo
git clone https://github.com/MSWEIMZ/agnes-mcp.git
cd agnes-mcp

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

## Running Tests

```bash
python -m pytest test_server.py -v
```

All tests must pass before submitting a PR.

## Making Changes

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Add tests for new functionality
5. Run tests: `python -m pytest test_server.py -v`
6. Commit with a clear message
7. Push and open a Pull Request

## Code Style

- Follow existing code patterns
- Use type hints
- Keep functions focused and well-documented
- Async functions for all HTTP operations

## Reporting Issues

- Use GitHub Issues
- Include steps to reproduce
- Include Python version and OS
- Include error messages / logs

## Adding New Tools

When adding a new MCP tool:

1. Add the internal implementation function (e.g., `generate_xxx`)
2. Add the `@mcp.tool()` wrapper with proper docstring
3. Add tests covering success, error, and edge cases
4. Update README tool table (both English and Chinese)
5. Bump version in `__init__.py`, `server.py`, `pyproject.toml`

## License

By contributing, you agree that your contributions will be licensed under the MIT License.