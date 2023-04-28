#migration_utils.py


import importlib
from typing import List

import alembic.config
from alembic import command, config
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError

from . import config
from .models import Base

engine = create_engine(config.DB_URL)

alembic_cfg = alembic.config.Config("./alembic.ini")
alembic_cfg.set_main_option("script_location", "./migrations")
alembic_cfg.set_main_option("sqlalchemy.url", str(engine.url))


def upgrade_database():
    """
    Применение миграций к текущей базе данных
    """
    with engine.connect() as conn:
        alembic_cfg.attributes["connection"] = conn
        command.upgrade(alembic_cfg, "head")


def downgrade_database():
    """
    Откат миграций на одну версию
    """
    with engine.connect() as conn:
        alembic_cfg.attributes["connection"] = conn
        command.downgrade(alembic_cfg, "-1")


def create_migration(message):
    """
    Генерация новой миграции на основании изменений в models.py
    """
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
    models_module = importlib.import_module("web.models")
    return Base.metadata.tables.keys()


def get_database_tables() -> List[str]:
    """
    Получение списка названий таблиц из текущей базы данных
    """
    inspector = engine.dialect.inspector(engine)
    return inspector.get_table_names()


def check_database():
    """
    Проверка соответствия текущей базы данных и models.py,
    добавление новых таблиц в базу данных при необходимости
    """
    models_tables = get_models_tables()
    database_tables = get_database_tables()

    missing_tables = set(models_tables) - set(database_tables)

    inspector = engine.dialect.inspector(engine)

    for table_name in missing_tables:
        if table_name in models_tables:
            if not inspector.has_table(table_name):
                table = Base.metadata.tables[table_name]
                try:
                    table.create(engine, checkfirst=True)
                except ProgrammingError:
                    pass  # таблица уже существует    

    upgrade_database()
