# Contributing to Quirky_Dweed

Thank you for your interest in contributing to Quirky_Dweed! We welcome contributions from the community and want to make the process as easy and transparent as possible.

## 🚀 Ways to Contribute

- **Reporting Bugs**: If you find a bug, please open an issue describing the problem and steps to reproduce.
- **Suggesting Enhancements**: Have an idea to make the Hub better? Open an issue with the "enhancement" label.
- **Pull Requests**:
    1. Fork the repository.
    2. Create a new branch for your feature or fix.
    3. Ensure your code follows the existing style and passes all tests.
    4. Submit a pull request with a clear description of your changes.

## 💻 Technical Guidelines

- **Style Guide**: Follow PEP 8 for Python code style.
- **Type Hints**: Use type hints for better code maintainability.
- **Templates**: Use Jinja2 templating with proper escaping.
- **Commit Messages**: Use [Conventional Commits](https://www.conventionalcommits.org/) (e.g., `feat: add character filter`, `fix: resolve mobile overflow`).

## 🛠️ Local Development

1. Fork and clone the repo.
2. Set up a virtual environment: `python -m venv venv`
3. Activate the environment: `source venv/bin/activate` (Windows: `venv\Scripts\activate`)
4. Install dependencies: `pip install -r requirements.txt`
5. Set up your `.env` file with Supabase credentials
6. Run the development server: `python main.py`
7. Test your changes and ensure they work correctly.
