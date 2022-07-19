pushd .
cd ..
call venv\Scripts\activate.bat
pre-commit run --all-files
popd
call deactivate
