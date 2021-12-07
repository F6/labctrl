CALL C:\ProgramData\Anaconda3\condabin\conda.bat activate base

set FLASK_APP=CDHD2_emulator
python -m flask run --port 5002
