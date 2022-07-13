CALL C:\ProgramData\Anaconda3\condabin\conda.bat activate base

set FLASK_APP=generic_server
python -m flask run --host=0.0.0.0 --port=5055

pause