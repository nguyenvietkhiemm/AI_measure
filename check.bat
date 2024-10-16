@echo off
echo Extracting requirements...
pip freeze > requirements.txt

echo Checking for uncommitted changes...
git status

rem
if not "%ERRORLEVEL%" == "0" (
    echo No changes to commit.
    pause
    exit /b
)

git add .

echo Preparing to push changes...
pause
