pushd .
cd ..
rmdir /S /Q dist
call venv\Scripts\activate.bat
pre-commit autoupdate
python -m build
popd
call deactivate
