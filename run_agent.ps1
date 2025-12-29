# PowerShell launcher for agent.py. Runs using .venv if available.
if (Test-Path -Path .\.venv\Scripts\Activate.ps1) {
    . .\.venv\Scripts\Activate.ps1
}
python agent.py $args
