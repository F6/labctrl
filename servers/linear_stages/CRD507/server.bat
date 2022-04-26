CALL C:\ProgramData\Anaconda3\condabin\conda.bat activate base

set FLASK_APP=CRD507_server
python -m flask run --host=0.0.0.0 --port=5005

pause