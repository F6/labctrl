CALL C:\ProgramData\Anaconda3\condabin\conda.bat activate base

set FLASK_APP=ziUHF_proxy
python -m flask run --host=0.0.0.0 --port=5013

pause