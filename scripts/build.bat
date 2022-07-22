pushd .
cd ..
rmdir /S /Q dist
call venv\Scripts\activate.bat
python yadd\make_versions_file.py
pre-commit autoupdate
python -m build
popd
call deactivate
