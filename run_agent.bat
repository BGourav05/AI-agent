@echo off
REM Launch agent using the project's virtualenv if present
IF EXIST ".venv\Scripts\activate.bat" (
    CALL .venv\Scripts\activate.bat
    python agent.py %*
) ELSE (
    python agent.py %*
)
PAUSE
