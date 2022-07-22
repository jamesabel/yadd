pushd .
cd ..
rmdir /S /Q dist
call venv\Scripts\activate.bat
python yadd\make_versions_file.py
python -m build
popd
call deactivate
