WHO (World Health Organization) Data App
=========================================

This is a library that will serve a data ingestion and parsing library
and web application which will store and search on open source data 
taken from the WHO website.


Requirements
------------
    Python3.5
    virtualenv


Setup
-----
    - clone repository and CD into base directory
	
    - create and activate a python3.5 virtual environment:
        $ virtualenv -p python3.5 virtual_env
	$ source virtual_env/bin/activate
	
    - install requirements:
	$ pip install -r requirements.txt

    - run setup.py:
	$ python setup.py develop

    - create database assets:
	$ psql postgres
	# create database <database-name>
	# \q

    - edit development.ini and alembic.ini to use your "database-name"
    - run alembic upgrades
	$ alembic upgrade head


Data Ingestion
--------------
To ingest data into the database, make sure you have CSV files that are mapped
in the file who_data.bin.ingest.bin.file_map

They should look something like:
Country,Reported cases; 2014,Reported cases; 2013,Reported cases; 2012 ....
United States, 7583, 8275, 2575 ....

Run the ingest script and pass in an INI file for the configuration of the 
database you wish to populate:
    $ python who_data/bin/ingest/ingest.py development.ini


Tests
-----
Run tests with the nosetests command or run tests for a specific function.

Tests are located in directory closest to the thing they test.
Example, to run pyramid app tests:
    $ nosetests who_data/tests

To run ingest module tests:
    $ nosetests who_data/bin/ingest/tests


Linting
-------
This repository is linted using the standard flake8 library,
ignoring error codes E402 and E711:

    $ flake8 --ignore=E402,E711


Running the application
-----------------------
With the virtual environment activated, update development.ini to match
your database configuration, run with paster:
    
    $ pserve development.ini

Navigate to an API url, such as:
    http://localhost:<your-port-number/who-data/api/v1/countries
