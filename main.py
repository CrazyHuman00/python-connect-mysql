"""FastAPIを用いたAPIの作成、データベースの操作を行うプログラム"""

# /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Asakura Hiroto'
__version__ = '1.0.0'
__date__ = '2024/10/19 (Created: 2024/09/30)'

import sqlite3
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

app = FastAPI()
jinja_template = Jinja2Templates(directory='frontend') # jinja2テンプレートのhtmlファイルを収める場所

DATABASE_FILE  = 'database/prompt.db'
SQL_SHOW_TABLE = 'select * from prompt;'
SQL_GET_USER   = 'select * from prompt where user_name==?;'
SQL_INSERT     = 'insert into prompt (user_name, like_food) values (?,?);'
SQL_UPDATE     = 'update prompt set user_name=?,like_food=? where user_name==?;'
SQL_DELETE     = 'delete from prompt where user_name==?;'


@app.get('/')
def index(request: Request):
    """_summary_
    インデックスページ

    Args:
        request (Request): リクエスト

    Returns:
        _TemplateResponse : テンプレートレスポンス
    """
    with sqlite3.connect(DATABASE_FILE) as conn:
        cur = conn.cursor()
        users_info = cur.execute(SQL_SHOW_TABLE).fetchall()
        parameter = {'request': request, 'users_info': users_info}
        return jinja_template.TemplateResponse('index.html', parameter)


@app.get('/user/{name}')
def user(request: Request, name: str):
    """_summary_
    各データ表示と編集のページ

    Args:
        request (Request): リクエスト
        name (str): ユーザ名

    Returns:
        _TemplateResponse : テンプレートレスポンス
    """
    with sqlite3.connect(DATABASE_FILE) as conn:
        cur = conn.cursor()
        user_info = cur.execute(SQL_GET_USER, [name]).fetchone()

        if user_info:
            parameter = {'request': request, 'user_name': user_info[0], 'like_food': user_info[1]}
            return jinja_template.TemplateResponse('user.html', parameter)

        parameter = {'request': request,'error_message': 'このページは存在しないか、削除されました'}
        return jinja_template.TemplateResponse('error.html', parameter)


@app.post('/register')
async def register(request: Request):
    """_summary_
    新しいデータ登録する処理

    Args:
        request (Request): リクエスト

    Returns:
        _RedirectResponse : リダイレクトレスポンス

    Raises:
        sqlite3.Error : データベースエラー
    """
    try:
        with sqlite3.connect(DATABASE_FILE) as conn:
            form = await request.form()
            user_name, like_food = form['user_name'], form['like_food']
            cur = conn.cursor()
            cur.execute(SQL_INSERT,(user_name, like_food))
        return RedirectResponse(url='/', status_code=303)
    except sqlite3.Error as err:
        parameter = {'request': request, 'error_message': f'エラー：{type(err)} {err}'}
        return jinja_template.TemplateResponse('error.html', parameter)


@app.post('/renew/{name}')
async def renew(request: Request):
    """_summary_
    データ更新する処理

    Args:
        request (Request): リクエスト

    Returns:
        RedirectResponse: リダイレクトレスポンス
    
    Raises:
        sqlite3.Error: データベースエラー
    """
    try:
        with sqlite3.connect(DATABASE_FILE) as conn:
            form = await request.form()
            user_name, like_food = form['user_name'], form['like_food']
            cur = conn.cursor()
            cur.execute(SQL_UPDATE,(user_name, like_food, user_name))
        return RedirectResponse(url='/', status_code=303)
    except sqlite3.Error as err:
        parameter = {'request': request, 'error_message': f'エラー：{type(err)} {err}'}
        return jinja_template.TemplateResponse('error.html', parameter) # なにか間違いがある場合


@app.post('/delete')
async def delete(request: Request):
    """_summary_
    データ削除する処理

    Args:
        request (Request): リクエスト

    Returns:
        RedirectResponse: リダイレクトレスポンス
    
    Raises:
        sqlite3.Error: データベースエラー
    """
    try:
        with sqlite3.connect(DATABASE_FILE) as conn:
            form = await request.form()
            user_name = form['user_name']

            cur = conn.cursor()
            cur.execute(SQL_DELETE,[user_name])

        return RedirectResponse(url='/',status_code=303) # インデックスページに戻る
    except sqlite3.Error as err:
        parameter = {'request': request, 'error_message': f'エラー：{type(err)} {err}'}
        return jinja_template.TemplateResponse('error.html', parameter) # なにか間違いがある場合


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """_summary_
    エラーハンドリング

    Args:
        request (Request): リクエスト
        exc (str): エラーメッセージ

    Returns:
        _TemplateResponse : テンプレートレスポンス
    """
    parameter = {'request': request, 'error_message': exc}
    return jinja_template.TemplateResponse('error.html', parameter)
