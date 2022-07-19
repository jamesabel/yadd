call build.bat
pushd .
cd ..
call venv\Scripts\activate.bat
REM
REM twine upload -r testpypi dist/*
twine upload dist/*
call deactivate
popd
