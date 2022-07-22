pushd .
cd ..
call venv\Scripts\activate.bat
pre-commit autoupdate
pre-commit run --all-files
popd
call deactivate
