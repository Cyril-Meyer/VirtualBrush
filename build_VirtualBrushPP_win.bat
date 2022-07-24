cd VirtualBrushPP
rmdir /s /q build
python setup.py build
cd ..
copy VirtualBrushPP\build\lib.win-amd64-3.7\VirtualBrushPP.cp37-win_amd64.pyd VirtualBrushPP.pyd
pause
