@echo off

rem 
call venv\Scripts\activate.bat
echo ACTIVATED

rem 
echo System is running...
cd src
python index.py

jupyter notebooks/exploration.ipynb
jupyter notebooks/analysis.ipynb

rem 
cd ..
call venv\Scripts\deactivate.bat
echo DEACTIVATED

echo DONE
pause
