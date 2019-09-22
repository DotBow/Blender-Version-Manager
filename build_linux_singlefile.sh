PYTHONOPTIMIZE=2 /home/oleg/.local/bin/pyinstaller \
--clean \
--noconsole \
--noupx \
--onefile \
--windowed \
--icon="icons\app_inv.ico" \
--name="Blender Version Manager" \
--version-file="version.txt" \
main.py