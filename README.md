# rest-api-prototype

## Requirements

- Python 3.6+
- conda (or something similar to create a Python environment for running the tests)
- git (only to clone this repository)
- Docker (only if you want to run the tests against a MySQL container which is automatically handled by the tests)

## Run tests
The commands below set everything up to run the tests with default options. The database is torn down and recreated for each
test module.

```
$ git clone https://github.com/hnluu8/rest-api-prototype.git
$ cd rest-api-prototype
$ conda create -p venv python=3.7 
$ conda activate venv/
(venv) pip install -r requirements.txt
(venv) pytest --verbose --capture=no community/tests
```

### Test options

#### --fallback_db_uri
The conftest.py will attempt to pull a MySQL docker image and run the container to act as the database engine for the tests.
In the event the container fails to run, the tests will fallback to the database specified by the test option **--fallback_db_uri**
which defaults to 'sqlite:///:memory:'. To specify a different fallback database engine, just pass it to pytest when running the
tests:

```
(venv) pytest --verbose --capture=no community/tests --fallback_db_uri=mysql+pymysql://root:@localhost:3306/community'
```

If you choose any other database engine besides MySQL, you'll have to install the additional pip dependencies yourselves.
Also, the fallback_db_uri has to be in the same format as SQLALCHEMY_DATABASE_URI.

Again, this only comes into play if you don't have Docker on your machine and you don't care for SQLite in-memory database.

#### --host_port
By default, the MySQL container port is mapped to port 3306 on your host machine. Change this test option if you want to map the 
MySQL container port to something else on your host machine to avoid possible conflicts.

```
(venv) pytest --verbose --capture=no community/tests --host_port=10000
```

