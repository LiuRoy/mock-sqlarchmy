# -*- coding=utf8 -*-
from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite://')
MockSession = sessionmaker(bind=engine)


def create_table(table):
    """内存数据库中建表

    Args:
        table (sqlalchemy.ext.declarative.api.DeclarativeMeta): 表定义类
    """
    super_class = table.mro()[1]
    super_class.metadata.create_all(bind=engine, tables=[table.__table__])
    return True


def create_tables(tables):
    """内存数据库中建表

    Args:
        table (list): 表定义类
    """
    for table_class in tables:
        super_class = table_class.mro()[1]
        super_class.metadata.create_all(
            bind=engine,
            tables=[table_class.__table__]
        )
    return True


def drop_table(table):
    """内存数据库中建表

    Args:
        table (sqlalchemy.ext.declarative.api.DeclarativeMeta): 表定义类
    """
    super_class = table.mro()[1]
    super_class.metadata.drop_all(bind=engine, tables=[table.__table__])
    return True


def drop_tables(tables):
    """内存数据库中建表

    Args:
        table (list): 表定义类
    """
    for table_class in tables:
        super_class = table_class.mro()[1]
        super_class.metadata.drop_all(
            bind=engine,
            tables=[table_class.__table__]
        )
    return True


def mock_deco(monkeypatch, session_list, table_list):
    """
    testcase装饰器, 在运行测试前创建表
    """
    def deco(func):
        @wraps(func)
        def _inner(*args, **kwargs):
            create_tables(table_list)
            for module, session in session_list:
                monkeypatch.setattr(module, session, MockSession)

            result = func(*args, **kwargs)
            drop_tables(table_list)
            return result

        return _inner

    return deco
