PYTHON = python
PYLINT = pylint
PYDOC = pydoc
FRONTEND_DIR = $(shell pwd)/frontend
BACKEND_DIR = $(shell pwd)/backend
DATABASE_DIR = $(shell pwd)/database
WORKING_DIR = $(shell pwd)

# create the database
create: 
	$(PYTHON) $(DATABASE_DIR)/create_database.py

# run the fastapi server
run:
	(cd $(BACKEND_DIR) && uvicorn main:app --reload)

# run the frontend
web:
	(cd $(FRONTEND_DIR) && open http://127.0.0.1:5500/frontend/index.html)

# pylint the backend
lint:
	(cd $(BACKEND_DIR) && pylint *.py)