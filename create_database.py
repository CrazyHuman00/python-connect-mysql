# /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'asakura hiroto'
__version__ = '1.0.0'
__date__ = '2024/09/30 (Created: 2024/09/30)'

from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URI = 'sqlite:///database/prompt.db'

engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={'check_same_thread': False}, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# テーブルの定義
class Prompt(Base):
    """
    Promptテーブルの定義
    Args:
        Base (declarative_base): テーブルのベースクラス
    """
    # テーブル名
    __tablename__ = 'prompt'
    # ユーザ名
    user_name = Column('user_name', String(100), primary_key=True)
    # 好きな食べ物
    like_food = Column('like_food', String(500))


# テーブル作成
Base.metadata.create_all(bind=engine)