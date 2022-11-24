CALL C:\ProgramData\Anaconda3\condabin\conda.bat activate base

set FLASK_APP=ziUHF_sync_emulator
python -m flask run --host=0.0.0.0 --port=5060

pause