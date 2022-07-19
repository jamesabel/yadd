echo on
pushd .
cd ..
rmdir /S /Q venv
"\Program Files\Python311\python.exe" -m venv --clear venv
call venv\Scripts\activate.bat
python -m pip install --no-deps --upgrade pip
python -m pip install -U setuptools
python -m pip install -U -r requirements-dev.txt
pre-commit install
popd
call deactivate
