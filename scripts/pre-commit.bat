pushd .
cd ..
call venv\Scripts\activate.bat
REM pre-commit autoupdate
pre-commit run --all-files
popd
call deactivate
