# /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Asakura Hiroto'
__version__ = '1.0.0'
__date__ = '2024/10/19 (Created: 2024/09/30)'

"""
FastAPIを用いたAPIの作成
"""

import os,sqlite3
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

app = FastAPI()
jinja_template = Jinja2Templates(directory='frontend') # jinja2テンプレートのhtmlファイルを収める場所

database_file  = 'database/prompt.db'
SQL_SHOW_TABLE = 'select * from prompt;'
SQL_GET_USER   = 'select * from prompt where user_name==?;'
SQL_INSERT     = 'insert into prompt (user_name, like_food) values (?,?);'
SQL_UPDATE     = 'update prompt set user_name=?,like_food=? where user_name==?;'
SQL_DELETE     = 'delete from prompt where user_name==?;'


# インデックスページ
@app.get('/')
def index(request: Request):
    with sqlite3.connect(database_file) as conn:
        cur = conn.cursor()
        users_info = cur.execute(SQL_SHOW_TABLE).fetchall()
        parameter = {'request': request, 'users_info': users_info}
        return jinja_template.TemplateResponse('index.html', parameter)

# 各データ表示と編集のページ
@app.get('/user/{name}')
def user(request: Request, name: str):
    with sqlite3.connect(database_file) as conn:
        cur = conn.cursor()
        user_info = cur.execute(SQL_GET_USER, [name]).fetchone()

        if(user_info):
            parameter = {'request': request, 'user_name': user_info[0], 'like_food': user_info[1]}
            return jinja_template.TemplateResponse('user.html', parameter)
        else:
            parameter = {'request': request,'error_message': 'このページは存在しないか、削除されました'}
            return jinja_template.TemplateResponse('error.html', parameter)

# 新しいデータ登録する処理
@app.post('/register')
async def register(request: Request):
    try:
        with sqlite3.connect(database_file) as conn:
            form = await request.form() 
            user_name, like_food = form['user_name'], form['like_food']
            cur = conn.cursor()
            cur.execute(SQL_INSERT,(user_name, like_food))
        return RedirectResponse(url='/', status_code=303)
    except Exception as err:
        parameter = {'request': request, 'error_message': f'エラー：{type(err)} {err}'}
        return jinja_template.TemplateResponse('error.html', parameter) 

# データ更新する処理
@app.post('/renew/{name}')
async def renew(request: Request):
    try:
        with sqlite3.connect(database_file) as conn:
            form = await request.form()
            user_name, like_food = form['user_name'], form['like_food']
            cur = conn.cursor()
            cur.execute(SQL_UPDATE,(user_name, like_food, user_name))
        return RedirectResponse(url='/', status_code=303) 
    except Exception as err:
        parameter = {'request': request, 'error_message': f'エラー：{type(err)} {err}'}
        return jinja_template.TemplateResponse('error.html', parameter) # なにか間違いがある場合

# データ削除する処理
@app.post('/delete')
async def delete(request: Request):
    try:
        with sqlite3.connect(database_file) as conn:
            form = await request.form()
            user_name = form['user_name']

            cur = conn.cursor()
            cur.execute(SQL_DELETE,[user_name])

        return RedirectResponse(url='/',status_code=303) # インデックスページに戻る
    except Exception as err:
        parameter = {'request': request, 'error_message': f'エラー：{type(err)} {err}'}
        return jinja_template.TemplateResponse('error.html', parameter) # なにか間違いがある場合

# エラーハンドリング
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    parameter = {'request': request, 'error_message': exc}
    return jinja_template.TemplateResponse('error.html', parameter)