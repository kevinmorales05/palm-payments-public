# Watch for documentation
http://127.0.0.1:8000/docs

# run project

uvicorn app.main:app --reload

# install dependencies
--- pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv alembic pydantic-settings

pip freeze > requirements.txt
pip install 
# run db
psql -U postgres
CREATE DATABASE fastapi_db;

# run the app in the server
uvicorn app.main:app --reload


# quemar dependencias en requirements.txt
pip freeze > requirements.txt

# usar un ambiente virtual
# Crear entorno virtual llamado "venv"
python -m venv venv

# Activar entorno virtual
# macOS/Linux
source venv/bin/activate

# conectarme al sql
docker exec -it ruku-db-1  psql -U postgres



## HOW TO download dependencies and run the project
# 1. create a virtual environment
python3 -m venv venv
# 2. Choose a virtual environment
# En Mac/Linux
source venv/bin/activate
# En Windows
venv\Scripts\activate
# 3. install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Run the project 
uvicorn app.main:app --reload
