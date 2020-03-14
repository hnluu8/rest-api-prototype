import dependency_injector.containers as containers
import dependency_injector.providers as providers
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from logging import Logger
from sqlalchemy.orm.scoping import ScopedSession
from community.dao.community import CommunityDao
from community.service.community import CommunityService


class IocContainer(containers.DeclarativeContainer):
    """
        Define dependencies and inject them into data and service layers when creating Flask app.
    """

    config = providers.Configuration('config', default={
        'SQLALCHEMY_DATABASE_URI': 'mysql+pymysql://root:@localhost/community',
        'LOG_PATH': 'rest-api-prototype.log',
        'SQLALCHEMY_ECHO': True,
        'CACHE_TYPE': 'simple',
        'CACHE_DEFAULT_TIMEOUT': 300
    })

    app = providers.Factory(Flask, __name__)

    cache = providers.Dependency(instance_of=Cache)

    logger = providers.Dependency(instance_of=Logger)

    db = providers.Dependency(instance_of=SQLAlchemy)

    db_session = providers.Dependency(instance_of=ScopedSession)

    community_dao = providers.Dependency(instance_of=CommunityDao)

    community_service = providers.Singleton(CommunityService, community_dao, logger)
