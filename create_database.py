"""データベースを作成するプログラム"""

# /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Asakura Hiroto'
__version__ = '1.0.0'
__date__ = '2024/10/19 (Created: 2024/09/30)'

from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base

SQLALCHEMY_DATABASE_URI = 'sqlite:///database/prompt.db'
Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URI)

class Prompt(Base):
    """
    Promptテーブルの定義
    """

    # テーブル名
    __tablename__ = 'prompt'
    # ユーザ名
    user_name = Column('user_name', String(100), primary_key=True)
    # 好きな食べ物
    like_food = Column('like_food', String(500))

Base.metadata.create_all(bind=engine)
