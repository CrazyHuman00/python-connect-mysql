# /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Asakura Hiroto'
__version__ = '2.0.0'
__date__ = '2024/12/16 (Created: 2024/09/30)'

""" FastAPIを用いたAPIの作成、データベースの操作を行うプログラム """

from app.create_database import Database
from app.api import APIApp

def main():
    """ メイン関数 """
    # データベースの作成
    user_name = 'user_name'
    like_food = 'like_food'
    create_database = Database(user_name, like_food)
    create_database.create_table()

    # APIの起動
    api_app = APIApp()
    api_app.run()

if __name__ == '__main__':
    main()
