#migration_utils.py


import importlib
from typing import List

from alembic import command, config
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine

from . import models
from .models import Base
from .base import Base

from . import config
from .config import DB_URL

engine = create_engine(DB_URL)


def upgrade_database(engine):
    """
    Применение миграций к текущей базе данных
    """
    alembic_cfg = config.Config("./alembic.ini")
    alembic_cfg.set_main_option("script_location", "= ./migrations")
    alembic_cfg.set_main_option("sqlalchemy.url", str(engine.url))

    with engine.connect() as conn:
        alembic_cfg.attributes["connection"] = conn
        print
        command.upgrade(alembic_cfg, "head")


def create_migration(message):
    """
    Генерация новой миграции на основании изменений в models.py
    """
    engine = create_engine(str(models.db_url))
    alembic_cfg = config.Config("./alembic.ini")
    alembic_cfg.set_main_option("script_location", "= ./migrations")
    alembic_cfg.set_main_option("sqlalchemy.url", str(engine.url))

    with engine.connect() as conn:
        alembic_cfg.attributes["connection"] = conn
        script_dir = ScriptDirectory.from_config(alembic_cfg)
        head_revision = script_dir.get_current_head()
        revisions = [x.revision for x in ScriptDirectory.from_config(alembic_cfg).walk_revisions()]

        if head_revision in revisions:
            raise ValueError("Head revision already in revision history")

        command.revision(alembic_cfg, message=message, autogenerate=True)


def get_models_tables() -> List[str]:
    """
    Получение списка названий таблиц из models.py
    """
    models_module = importlib.import_module(". models")
    Base.metadata.create_all(bind=create_engine(str(models.db_url)), checkfirst=False)
    return Base.metadata.tables.keys()


def get_database_tables(engine) -> List[str]:
    """
    Получение списка названий таблиц из текущей базы данных
    """
    inspector = engine.dialect.inspector(engine)
    return inspector.get_table_names()


def check_database(engine):
    """
    Проверка соответствия текущей базы данных и models.py,
    добавление новых таблиц в базу данных при необходимости
    """
    engine = create_engine(str(models.db_url))
    models_tables = get_models_tables()
    database_tables = get_database_tables(engine)

    missing_tables = set(models_tables) - set(database_tables)

    for table_name in missing_tables:
        table = Base.metadata.tables[table_name]
        table.create(engine)

    upgrade_database(engine)
