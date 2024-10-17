@echo off

rem 
call venv\Scripts\activate.bat
echo ACTIVATED

rem 
echo System is running...
cd src
python index.py
echo The system has finished running

echo Notebooks is running...
jupyter nbconvert --to script --execute --inplace --ExecutePreprocessor.timeout=-1 ./notebooks/*.ipynb
echo Notebooks have finished running

rem 
cd ..
call venv\Scripts\deactivate.bat
echo DEACTIVATED

echo DONE
pause
