# Contributing to CodeGuard

We love contributions! Here's how you can help make CodeGuard better.

## 🚀 Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/codeguard.git
   cd codeguard
   ```
3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## 🧪 Before You Code

- Check [open issues](https://github.com/mohameden19961/codeguard/issues) for something to work on
- For new features, open an issue first to discuss the design
- For bugs, comment on the issue to let others know you're working on it

## 💻 Development Workflow

1. Create a branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Write code and tests
3. Run tests:
   ```bash
   pytest tests/ -v
   ```
4. Run linting:
   ```bash
   ruff check src/codeguard/
   ```
5. Commit with a descriptive message:
   ```bash
   git commit -m "Add feature X that does Y"
   ```
6. Push and create a Pull Request

## 📝 Commit Guidelines

- Use present tense ("Add feature" not "Added feature")
- Reference issues: `Refs: #123` or `Fixes: #123`
- Keep commits focused on a single change

## 🧪 Testing Guidelines

- Write tests for all new functionality
- Use pytest fixtures for reusable test setup
- Aim for >80% coverage on new code
- Test edge cases (empty files, invalid input, etc.)

## 📚 Documentation

- Update docs when changing behavior
- Add docstrings to new public functions/classes
- Include code examples in docstrings

## 🔍 Pull Request Process

1. Ensure all tests pass
2. Update CHANGELOG.md with your changes
3. Add yourself to contributors if desired
4. Request review from maintainers
5. Address review feedback

---

Thank you for contributing! 🎉
