@echo off
:: Terminate all Python processes
taskkill /F /IM python.exe 2>nul

:: Change to the SpyNet directory and run git pull
cd "C:\Users\Spy\Downloads\SpyNet"
git pull

:: Run the Python script
python.exe "C:\Users\Spy\Downloads\SpyNet\main.py"


taskkill /F /IM python.exe 2>nul make it close the main.py only

