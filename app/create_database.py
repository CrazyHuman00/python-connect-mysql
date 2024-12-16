# /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Asakura Hiroto'
__version__ = '2.0.0'
__date__ = '2024/10/19 (Created: 2024/09/30)'

""" データベースを作成するプログラム"""

import os
import sqlite3

class Database():
    """ データベースを作成するクラス """

    def __init__(self, user_name, like_food):
        """ コンストラクタ """
        self.__tablename__ = 'users'
        self.db_path = 'database'
        self.user_name = user_name
        self.like_food = like_food

    def __repr__(self):
        return f'<Prompt(user_name={self.user_name}, like_food={self.like_food})>'

    def create_table(self):
        """ テーブルを作成する """
        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path, exist_ok=True)
        db_file = os.path.join(self.db_path, self.__tablename__ + '.db')
        with sqlite3.connect(db_file) as conn:
            conn.execute(
                f'create table if not exists {self.__tablename__} (user_name text primary key, like_food text);'
            )
