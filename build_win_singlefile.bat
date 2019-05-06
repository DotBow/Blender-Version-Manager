if exist __pycache__ rd /S /Q __pycache__
if exist build rd /S /Q build
if exist dist rd /S /Q dist
if exist "Blender Version Manager.spec" del /Q "Blender Version Manager.spec"

python -OO -m PyInstaller ^
--noconsole ^
--noupx ^
--onefile ^
--windowed ^
--uac-admin ^
--icon="icons\app_inv.ico" ^
--name="Blender Version Manager" ^
--version-file="version.txt" ^
main.py

pause