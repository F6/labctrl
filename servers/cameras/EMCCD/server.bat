CALL C:\ProgramData\Anaconda3\condabin\conda.bat activate base

set FLASK_APP=ccd_server
python -m flask run --host=0.0.0.0 --port=5007

pause