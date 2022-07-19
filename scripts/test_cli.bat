pushd .
cd ..
call venv\Scripts\activate.bat
python -m yadd test_yadd\data\expected.json test_yadd\data\uut_pass.json
popd
call deactivate
