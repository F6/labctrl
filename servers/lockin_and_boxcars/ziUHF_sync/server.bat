CALL C:\ProgramData\Anaconda3\condabin\conda.bat activate base

set FLASK_APP=ziUHF_sync_server
python -m flask run --host=127.0.0.1 --port=5060

pause