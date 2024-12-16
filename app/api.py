# /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Asakura Hiroto'
__version__ = '2.0.0'
__date__ = '2024/12/16 (Created: 2024/12/16)'

""" FastAPIを使ったAPIサーバー """

import sqlite3
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import uvicorn

class APIApp:
    """ FastAPIを使ったAPIサーバー """

    # データベース操作用のSQL文
    DATABASE_FILE  = 'database/users.db'
    SQL_SHOW_TABLE = 'select * from users;'
    SQL_GET_USER   = 'select * from users where user_name==?;'
    SQL_INSERT     = 'insert into users (user_name, like_food) values (?,?);'
    SQL_UPDATE     = 'update users set user_name=?,like_food=? where user_name==?;'
    SQL_DELETE     = 'delete from users where user_name==?;'


    def __init__(self):
        """ コンストラクタ"""
        self.app = FastAPI()
        self.jinja_template = Jinja2Templates(directory='frontend') # jinja2テンプレートのhtmlファイルを収める場所


    def index(self, request: Request):
        """ インデックスページ """
        with sqlite3.connect(self.DATABASE_FILE) as conn:
            cur = conn.cursor()
            users_info = cur.execute(self.SQL_SHOW_TABLE).fetchall()
            parameter = {'request': request, 'users_info': users_info}
            return self.jinja_template.TemplateResponse('index.html', parameter)


    def user(self, request: Request, name: str):
        """ 各データ表示と編集のページ """
        with sqlite3.connect(self.DATABASE_FILE) as conn:
            cur = conn.cursor()
            user_info = cur.execute(self.SQL_GET_USER, [name]).fetchone()
            if user_info:
                parameter = {'request': request,
                            'user_name': user_info[0], 
                            'like_food': user_info[1]}
                return self.jinja_template.TemplateResponse('user.html', parameter)

        parameter = {'request': request,'error_message': 'このページは存在しないか、削除されました'}
        return self.jinja_template.TemplateResponse('error.html', parameter)


    async def resist_data(self, request: Request):
        """ データの登録 """
        try:
            with sqlite3.connect(self.DATABASE_FILE) as conn:
                form = await request.form()
                user_name, like_food = form['user_name'], form['like_food']
                cur = conn.cursor()
                cur.execute(self.SQL_INSERT,(user_name, like_food))
                return RedirectResponse(url='/', status_code=303)
        except sqlite3.Error as err:
            parameter = {'request': request, 'error_message': f'エラー：{type(err)} {err}'}
            return self.jinja_template.TemplateResponse('error.html', parameter)


    async def update_data(self, request: Request):
        """ データの更新 """
        try:
            with sqlite3.connect(self.DATABASE_FILE) as conn:
                form = await request.form()
                user_name, like_food = form['user_name'], form['like_food']
                cur = conn.cursor()
                cur.execute(self.SQL_UPDATE,(user_name, like_food, user_name))
                return RedirectResponse(url='/', status_code=303)
        except sqlite3.Error as err:
            parameter = {'request': request, 'error_message': f'エラー：{type(err)} {err}'}
            return self.jinja_template.TemplateResponse('error.html', parameter)


    async def delete_data(self, request: Request):
        """ データの削除 """
        try:
            with sqlite3.connect(self.DATABASE_FILE) as conn:
                form = await request.form()
                user_name = form['user_name']
                cur = conn.cursor()
                cur.execute(self.SQL_DELETE,(user_name,))
                return RedirectResponse(url='/', status_code=303)
        except sqlite3.Error as err:
            parameter = {'request': request, 'error_message': f'エラー：{type(err)} {err}'}
            return self.jinja_template.TemplateResponse('error.html', parameter)


    async def validation_exception_handler(self, request, exc):
        """ バリデーションエラーのハンドラ """
        parameter = {'request': request, 'error_message': exc}
        return self.jinja_template.TemplateResponse('error.html', parameter)


    def run(self):
        """ サーバーを起動する """
        @self.app.get('/')
        def index(request: Request):
            return self.index(request)

        @self.app.get('/user/{name}')
        def user(request: Request, name: str):
            return self.user(request, name)

        @self.app.post('/resist_data')
        async def resist_data(request: Request):
            return await self.resist_data(request)

        @self.app.post('/update_data')
        async def update_data(request: Request):
            return await self.update_data(request)

        @self.app.post('/delete_data')
        async def delete_data(request: Request):
            return await self.delete_data(request)

        uvicorn.run(self.app, host="127.0.0.1", port=8000)
