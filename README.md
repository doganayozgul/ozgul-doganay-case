# QA Automation Case

Automated end-to-end test suite for the QA Hiring Case Study. Validates the complete QA job application flow including navigation, filtering, job list verification, and redirecting to the Lever application form page.

## Features

- ✅ Page Object Model (POM) architecture with separate Page Object classes
- ✅ Robust error handling and fallback mechanisms for UI variations
- ✅ Supports both positive and empty-state scenarios
- ✅ Automatic cookie banner handling
- ✅ Dynamic empty-state detection
- ✅ Explicit waits (WebDriverWait) for reliable element interaction
- ✅ Robust locators using `normalize-space` and `contains` for stable element finding

## Tech Stack

- **Python** 3.8+
- **Selenium WebDriver**
- **Pytest**
- **webdriver-manager**

## Requirements

- Python 3.8 or higher
- Chrome Browser (latest version)
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   cd ozgul_doganay_case
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   # .venv\Scripts\activate   # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install selenium pytest webdriver-manager
   ```

ChromeDriver is automatically managed by `webdriver-manager` - no manual installation required.

## Usage

### Run Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_insider_qa_flow.py

# Run with detailed output
pytest -v -s
```

### Advanced Options

```bash
# Generate HTML report
pytest --html=report.html --self-contained-html

# Run only failed tests
pytest --lf

# Show test names only
pytest --collect-only
```

## Test Scenario

The automated test performs the following steps:

1. **Home Page** - Navigates to `https://insiderone.com/`, accepts cookies, validates page title
2. **QA Careers Page** - Navigates to `https://insiderone.com/careers/quality-assurance/` page and validates page load
3. **Filtering** - Clicks "See all QA jobs", applies filters (Location: Istanbul, Turkey; Department: Quality Assurance)
4. **Job Validation** - Validates each job card contains correct Position, Department, and Location (if jobs exist)
5. **Lever Redirect** - Clicks "View Role" and verifies redirection to Lever application form
6. **Empty State** - Handles "Content is not available" scenario gracefully

The test passes in both scenarios: when jobs exist and when the list is empty.

## Project Structure

```
project/
├── pages/
│   ├── base_page.py          # Base page with common utilities
│   ├── home_page.py          # Home page object
│   ├── qa_page.py            # QA careers page object
│   └── lever_job_page.py     # Lever application page object
├── tests/
│   └── test_insider_qa_flow.py  # Main test file
├── conftest.py               # Pytest configuration
└── README.md
```

## Troubleshooting

### ChromeDriver Error
ChromeDriver is automatically managed. Ensure Chrome browser is up to date.

### Virtual Environment Not Active
```bash
source .venv/bin/activate  # Check for (.venv) prefix in terminal
```

### Import Errors
```bash
pip install --upgrade selenium pytest webdriver-manager
```

### Test Timeout
- Check internet connection
- Ensure Chrome browser is up to date
- Page loading may take time - wait for elements

## Notes

This test suite handles real-world UI variations gracefully. If job postings become available in the future, the same test will automatically switch to positive flow validation without code changes.
