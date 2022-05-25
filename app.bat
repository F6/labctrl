CALL C:\ProgramData\Anaconda3\condabin\conda.bat activate base
python -m bokeh serve apps/kerr_gating --show --keep-alive 10000 --check-unused-sessions 1000 --unused-session-lifetime 1000

@REM pause