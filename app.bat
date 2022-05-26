CALL C:\ProgramData\Anaconda3\condabin\conda.bat activate base
@REM For different users to share the same doc, they need to connect to the same session. This can be achieved by removing the --show option, and everyone access the same session by visit the same link http://localhost:5006/app_name?bokeh-session-id=whatever
python -m bokeh serve apps/pump_probe --show --keep-alive 10000 --check-unused-sessions 1000 --unused-session-lifetime 1000

@REM pause