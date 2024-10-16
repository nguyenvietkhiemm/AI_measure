@echo off

rem 
call venv\Scripts\activate.bat
echo ACTIVATED

rem 
python src\index.py
echo System is running...

rem 
call venv\Scripts\deactivate.bat
echo DEACTIVATED

echo DONE
pause
