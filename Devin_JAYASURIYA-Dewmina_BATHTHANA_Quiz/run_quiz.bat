@echo off
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Running quiz generator...
python soutenance_demo.py

pause
