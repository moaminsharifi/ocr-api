python3 -m pip install -r /usr/local/requirements.txt
python3 -m uvicorn main:app --port 8001 --host 0.0.0.0  --reload