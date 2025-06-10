@echo off 
echo. 
echo Se esta iniciando el proyecto

cd C:\proyectos_python\punto_venta


call .\venv\Scripts\deactivate


call .\venv\Scripts\activate

py manage.py runserver

pause