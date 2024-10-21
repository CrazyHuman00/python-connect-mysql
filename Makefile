PYTHON = python
PYLINT = pylint
PYDOC = pydoc
FRONTEND_DIR = $(shell pwd)/frontend
DATABASE_DIR = $(shell pwd)/database
WORKING_DIR = $(shell pwd)
LSOF = lsof -i :8000

# create the database
create: 
	($(PYTHON) create_database.py)

# run the fastapi server and open the docs
run:
	(($(PYTHON) create_database.py) && uvicorn main:app --reload --port 8000) &
	sleep 3; open http://localhost:8000

# pylint the backend
lint:
	$(PYLINT) *.py

port:
	$(LSOF)

clean:
	rm -rf $(DATABASE_DIR)/prompt.db