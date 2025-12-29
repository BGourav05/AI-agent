# PowerShell launcher to run the GUI agent via .venv (if present)
if (Test-Path -Path .\.venv\Scripts\Activate.ps1) {
    . .\.venv\Scripts\Activate.ps1
}
python gui_agent.py $args
