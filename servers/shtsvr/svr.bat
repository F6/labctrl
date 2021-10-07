CALL C:\ProgramData\Anaconda3\condabin\conda.bat activate base

set FLASK_APP=shtsvr
python -m flask run --host=0.0.0.0 --port=5002
