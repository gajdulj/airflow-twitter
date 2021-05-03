init:
	# Create python virtualenv & source it
	python3 -m venv .venv
	source .venv/bin/activate && pip list

install:
	# Install required dependencies
	source .venv/bin/activate &&\
		.venv/bin/pip install --upgrade pip &&\
		.venv/bin/pip install -r requirements.txt &&\
		pip list
	echo "Virtual environemnt created. Activate it with below:"
	echo "source .venv/bin/activate"
	
cleanup:
	# Destroy virtual environemnt. Adding dash on the beggining of the line ignores errors.
	# Therefore, this will still run fine even if some of the folders were deleted manually.
	-.venv/bin/pip uninstall -r requirements.txt -y
	- deactivate
	-rm -r .venv/

all: init install