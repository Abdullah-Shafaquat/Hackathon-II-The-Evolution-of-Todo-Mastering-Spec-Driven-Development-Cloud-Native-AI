@echo off
REM Test Runner Script for Windows
REM Runs all tests with coverage reporting

echo =========================================
echo Running Chat Endpoint Tests
echo =========================================
echo.

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)

REM Install test dependencies if needed
echo Installing test dependencies...
pip install -q pytest pytest-asyncio pytest-cov httpx

REM Run tests
echo.
echo Running tests...
pytest tests\ -v

REM Show coverage report
echo.
echo Coverage Summary:
pytest tests\ --cov=app --cov-report=term-missing

echo.
echo =========================================
echo Tests Complete!
echo =========================================
echo.
echo For detailed HTML coverage report:
echo   pytest tests\ --cov=app --cov-report=html
echo   Then open: htmlcov\index.html

pause
