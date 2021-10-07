CALL C:\ProgramData\Anaconda3\condabin\conda.bat activate base

set FLASK_APP=sht_emulator
python -m flask run --port 5002
