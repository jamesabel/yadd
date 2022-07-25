pushd .
cd ..
rmdir /S /Q dist
call venv\Scripts\activate.bat
python -m build
popd
call deactivate
