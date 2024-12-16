PYTHON = python
PYLINT = pylint
PYDOC = pydoc
APP_DIR = app
FRONTEND_DIR = frontend
DATABASE_DIR = database
DATABASE_NAME = users.db
CREATE_DATABASE = create_database.py
TARGET = main.py
WORKING_DIR = $(shell pwd)

test: clean

test:
	(cd $(APP_DIR) && $(PYTHON) $(CREATE_DATABASE)) \
	&& ($(PYTHON) main.py) \
	& (sleep 3; $ open http://127.0.0.1:8000)

lint:
	$(PYLINT) *.py $(APP_DIR)/*.py 

clean:
	rm -rf $(DATABASE_DIR)/*.db
	rm -rf $(APP_DIR)/__pycache__ $(FRONTEND_DIR)/__pycache__ $(DATABASE_DIR)/__pycache__ __pycache__