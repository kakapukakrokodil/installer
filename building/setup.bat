
::Enter your build code before this
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe' -OutFile %~dp0'\python-3.10.0-amd64.exe'"
python-3.10.0-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
pip install PySide6
python main.py