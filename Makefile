PYTHON = python
PYLINT = pylint
PYDOC = pydoc
FRONTEND_DIR = $(shell pwd)/frontend
DATABASE_DIR = $(shell pwd)/database
WORKING_DIR = $(shell pwd)

# create the database
create: 
	($(PYTHON) create_database.py)

# run the fastapi server and open the docs
run:
	(($(PYTHON) create_database.py) && uvicorn main:app --reload --port 8000)

# pylint the backend
lint:
	(pylint *.py)

clean:
	rm -rf $(DATABASE_DIR)/prompt.db