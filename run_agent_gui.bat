@echo off
REM Launch the GUI agent using the project's virtualenv if present
IF EXIST ".venv\Scripts\activate.bat" (
    CALL .venv\Scripts\activate.bat
    python gui_agent.py %*
) ELSE (
    python gui_agent.py %*
)
