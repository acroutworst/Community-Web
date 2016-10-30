@echo off
REM Community virtual environment setup script
REM ---------------------------------------------
REM Remove previous installation if exists
REM ---------------------------------------------
IF EXIST %~dp0.venv rmdir /s /q %~dp0.venv

REM ---------------------------------------------
REM Create .venv
ECHO creating virtual environment: .venv
python -m venv %~dp0.venv

REM ---------------------------------------------
ECHO activate .venv
call %~dp0.venv\Scripts\activate.bat

REM ---------------------------------------------
ECHO Installing requirements
pip install -r %~dp0requirements.txt

ECHO .venv setup complete. Virtual environment is activated.