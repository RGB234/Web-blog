@echo off
@cd D:\development\flaskProject\myarchive
@set FLASK_APP=myarchive
::development.py / production.py ->> development config choose
@set FLASK_ENV=development
@set APP_CONFIG_FILE=D:\development\flaskProject\myarchive\config\development.py
@D:\development\flaskProject\venvs\myarchive\Scripts\activate