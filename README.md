git clone https://github./flash-crud-app.git
cd flash-crud-app
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

pip install flask flask-sqlalchemy
python app.py
