import pytest
import docker
import time
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from community.dao import BaseModel
from community.dao.models.user import User
from community.dao.community import CommunityDao
from community.service.community import CommunityService
from community.api.flask import create_app
from community.api.container import IocContainer


def pytest_addoption(parser):
    parser.addoption('--mysql_image', action='store', default='mysql:8.0.19')
    parser.addoption('--host_port', action='store', default=3306)
    parser.addoption('--db_name', action='store', default='community')
    parser.addoption('--num_retries', action='store', default=10)
    parser.addoption('--fallback_db_uri', action='store', default='sqlite:///:memory:')


@pytest.fixture(scope='module')
def mysql_container(request):
    image = request.config.getoption('--mysql_image')
    host_port = request.config.getoption('--host_port')
    db_name = request.config.getoption('--db_name')
    container = None
    try:
        client = docker.from_env()
        print(f"Pulling Docker image {image}...please wait.")
        client.images.pull(image)
        container = client.containers.run(image,
                                      "--character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci",
                                      ports={'3306/tcp': host_port},
                                      name='rest-api-prototype-mysql',
                                      environment=['MYSQL_ALLOW_EMPTY_PASSWORD=yes', f'MYSQL_DATABASE={db_name}'],
                                      remove=True,
                                      detach=True)
        container.logs()
    except Exception as e:
        print(f"Attempt to run MySQL container failed: {e} - falling back to {request.config.getoption('--fallback_db_uri')}")
    return container


@pytest.fixture(scope='module')
def engine(request, mysql_container):
    if mysql_container is None:
        sqlalchemy_database_uri = request.config.getoption('--fallback_db_uri')
    else:
        host_port = request.config.getoption('--host_port')
        db_name = request.config.getoption('--db_name')
        sqlalchemy_database_uri = f'mysql+pymysql://root:@localhost:{host_port}/{db_name}'
    return create_engine(sqlalchemy_database_uri)


@pytest.fixture(scope='module')
def tables(request, mysql_container, engine):
    num_retries = request.config.getoption('--num_retries')
    while num_retries > 0:
        try:
            BaseModel.metadata.create_all(engine)
            break
        except OperationalError as e:
            num_retries -= 1
            print(f"Waiting for engine init to complete...")
            time.sleep(5)
            pass
    yield
    BaseModel.metadata.drop_all(engine)
    if mysql_container is not None:
        mysql_container.stop()


@pytest.fixture(scope='module')
def db_session(mysql_container, engine, tables):
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    session.add(User(username='jqpublic', name='John Q. Public'))
    session.add(User(username='jdoe', name='Jane Doe'))
    session.commit()

    yield session
    session.close()
    transaction.close()
    connection.close()


@pytest.fixture(scope='module')
def dao(db_session):
    return CommunityDao(db_session, logging)


@pytest.fixture(scope='module')
def service(dao):
    return CommunityService(dao, logging)


@pytest.fixture(scope='module')
def client(request, mysql_container):
    external_conf = None
    if mysql_container is None:
        external_conf = {
            'SQLALCHEMY_DATABASE_URI': request.config.getoption('--fallback_db_uri'),
            'TESTING': True,
            'DEBUG': True,
            'CACHE_TYPE': 'simple',
            'CACHE_DEFAULT_TIMEOUT': 300
        }
    app = create_app(external_conf)

    db = IocContainer.db()
    BaseModel.metadata.create_all(db.engine)

    db.session.add(User(username='jqpublic', name='John Q. Public'))
    db.session.add(User(username='jdoe', name='Jane Doe'))
    db.session.commit()

    with app.test_client() as client:
        yield client

    BaseModel.metadata.drop_all(db.engine)
