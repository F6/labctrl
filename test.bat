CALL C:\ProgramData\Anaconda3\condabin\conda.bat activate base
@REM For different users to share the same doc, they need to connect to the same session. This can be achieved by removing the --show option, and everyone access the same session by visit the same link http://localhost:5006/app_name?bokeh-session-id=whatever
<<<<<<< HEAD
python -m bokeh serve tests/linear_stages_bokeh --show --keep-alive 10000 --check-unused-sessions 10000 --unused-session-lifetime 10000
=======
python -m bokeh serve tests/figures_bokeh --show --keep-alive 10000 --check-unused-sessions 10000 --unused-session-lifetime 10000
>>>>>>> baf76103c22a246b39b356ad518692b63f59ecf2

pause