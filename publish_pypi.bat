@echo off
echo === Publishing agnes-mcp to PyPI ===
echo.
echo Step 1: Register at https://pypi.org/manage/account/token/
echo Step 2: Create an API token (scope: entire account)
echo Step 3: Run this script with your token:
echo   publish_pypi.bat YOUR_TOKEN_HERE
echo.
if "%~1"=="" (
    echo ERROR: No token provided.
    echo Usage: publish_pypi.bat YOUR_PYPI_TOKEN
    exit /b 1
)
set TWINE_USERNAME=__token__
set TWINE_PASSWORD=%~1
python -m build --wheel --no-isolation
python -m twine upload dist/* --non-interactive
echo.
echo Done! Check https://pypi.org/project/agnes-mcp/
