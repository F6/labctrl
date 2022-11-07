CALL C:\ProgramData\Anaconda3\condabin\conda.bat activate base

set FLASK_APP=toupcam_emulator
python -m flask run --port 5058

pause