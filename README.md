How to run API

1. cd to cloned dir
2. create virtual env: run "python -m venv venv"
3. activate venv: run "source venv/bin/activate"
4. install packages: run "pip install -r requirements.txt"
5. run "uvicorn app.main:app --reload"

Note: Even after running app locally, it won't function as
you would need to install and configure PostgreSQL locally
as this app connects to DB for CRUD operations
