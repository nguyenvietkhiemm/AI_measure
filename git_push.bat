@echo off
echo Extracting requirements...

call venv\Scripts\activate.bat
echo ACTIVATED

pip freeze > requirements.txt

call venv\Scripts\deactivate.bat
echo DEACTIVATED

echo Checking for uncommitted changes...
git status

rem Kiểm tra có thay đổi chưa
if not "%ERRORLEVEL%" == "0" (
    echo No changes to commit.
    pause
    exit /b
)

git add .

rem
set datetime=%DATE% %TIME%
set datetime=%datetime: =_%

git commit -m "fix_%datetime%"

git push

echo Preparing to push changes...
pause
