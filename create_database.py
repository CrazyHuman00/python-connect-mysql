# /usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module creates a SQLite database with a table named 'prompt'.
"""

__author__ = 'Asakura Hiroto'
__version__ = '1.0.0'
__date__ = '2024/10/19 (Created: 2024/09/30)'

from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base

SQLALCHEMY_DATABASE_URI = 'sqlite:///database/prompt.db'

class Prompt:
    """
    Promptテーブルの定義
    """

    # テーブル名
    __tablename__ = 'prompt'
    # ユーザ名
    user_name = Column('user_name', String(100), primary_key=True)
    # 好きな食べ物
    like_food = Column('like_food', String(500))

    def __init__(self, user_name: str, like_food: str):
        """_summary_
        コンストラクタ

        Args:
            user_name (str): ユーザ名
            like_food (str): 好きな食べ物
        """
        self.user_name = user_name
        self.like_food = like_food

    def __repr__(self):
        """_summary_
        ユーザ名と好きな食べ物を返す

        Returns:
            str: ユーザ名と好きな食べ物
        """
        return f'{self.user_name} likes {self.like_food}'


Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base.metadata.create_all(bind=engine)
