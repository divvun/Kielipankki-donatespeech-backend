# Recorder Backend API Tests

Comprehensive test suite for the Recorder Backend Lambda functions with mocked AWS S3 services.

## Test Coverage

- **Handler Endpoints** (`test_handler.py`): 16 tests
  - `POST /v1/init-upload` - Audio file upload initialization
  - `DELETE /v1/upload/{id}` - Client data deletion

- **Configuration Endpoints** (`test_configuration.py`): 12 tests
  - `GET /v1/configuration/{id}` - Single playlist loading
  - `GET /v1/configuration` - All playlists loading
  - YLE content URL mapping

- **Theme Endpoints** (`test_theme.py`): 11 tests
  - `GET /v1/theme/{id}` - Single theme loading
  - `GET /v1/theme` - All themes loading

**Total: 39 tests | 66% code coverage**

## Running Tests

### Quick Start

```bash
./run_tests.sh
```

### Manual Execution

```bash
# Activate virtual environment
source .venv/bin/activate

# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Run specific test file
pytest tests/test_handler.py -v

# Run specific test
pytest tests/test_handler.py::test_init_upload_success -v
```

## Test Data

Test fixtures use sample data from:
- `test/playlist.json` - Sample playlist configuration
- `test/theme.json` - Sample theme configuration

Mock S3 bucket is automatically created with test data during fixture setup.

## Coverage Report

After running tests, open the HTML coverage report:

```bash
open htmlcov/index.html
```

## Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Pytest fixtures and mocks
├── test_configuration.py    # Configuration endpoint tests
├── test_handler.py          # Handler endpoint tests
└── test_theme.py           # Theme endpoint tests
```

## Key Features

- **Mocked AWS S3**: Uses moto library for in-memory S3 simulation
- **No External Dependencies**: YLE API calls are mocked
- **Fast Execution**: All 39 tests complete in ~5 seconds
- **Isolated Tests**: Each test runs in isolated environment
- **Coverage Tracking**: Automatic code coverage reporting

## Continuous Integration

To integrate with CI/CD pipelines:

```yaml
# GitHub Actions example
- name: Run tests
  run: |
    pip install -r requirements.txt
    ./run_tests.sh
```

## Troubleshooting

### Import Errors
Ensure you're in the project root directory and virtual environment is activated.

### S3 Mocking Issues
Moto requires specific AWS credentials environment variables. The fixtures handle this automatically.

### YLE API Errors
YLE content mapping is automatically mocked in tests. If you see YLE-related errors, check the `mock_env` fixture in `conftest.py`.
