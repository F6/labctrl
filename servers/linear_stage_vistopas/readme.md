# Deployment Notice

the Adhon driver dll is a 32-bit program so only 32-bit python can load it,
so a embeded 32-bit python is needed to be placed under this directory and put
python.exe in a subdirectory named "python", or you can directly run the Flask
app with 32-bit python installed in your system. See svr.bat for more info.
