@echo off
@cd D:\development\flaskProject\myarchive
@set FLASK_APP=app

@REM D:\development\flaskProject\myarchive\app
@REM development.py / production.py    development config choose
@REM 'FLASK_ENV' is deprecated and will not be used in Flask 2.3. Use 'FLASK_DEBUG' instead.

@set FLASK_ENV=development
@set APP_CONFIG_FILE=D:\development\flaskProject\myarchive\config\development.py
@D:\development\flaskProject\venvs\myarchive\Scripts\activate
