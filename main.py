# /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'asakura hiroto'
__version__ = '1.0.0'
__date__ = '2024/09/30 (Created: 2024/09/30)'

"""
FastAPIを用いたAPIの作成
$ uvicorn main:app --reload
でサーバーを起動
"""

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session, sessionmaker
from starlette.requests import Request
from pydantic import BaseModel
from create_database import Prompt, engine

# DB接続用のセッションクラス インスタンスが作成されると接続する
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Pydanticを用いたAPIに渡されるデータの定義 ValidationやDocumentationの機能が追加される
class PromptIn(BaseModel):
    title: str
    done: bool

# 単一のPromptを取得するためのユーティリティ
def get_prompt(db_session: Session, prompt_id: int):
    return db_session.query(Prompt).filter(Prompt.id == prompt_id).first()

# DB接続のセッションを各エンドポイントの関数に渡す
def get_db(request: Request):
    return request.state.db

# このインスタンスをアノテーションに利用することでエンドポイントを定義できる
app = FastAPI()

# Promptの全取得
@app.get("/prompts/")
def read_prompts(db: Session = Depends(get_db)):
    prompts = db.query(Prompt).all()
    return prompts

# 単一のpromptを取得
@app.get("/prompts/{prompt_id}")
def read_prompt(prompt_id: int, db: Session = Depends(get_db)):
    prompt = get_prompt(db, prompt_id)
    return prompt

# Promptを登録
@app.post("/prompt/")
async def create_prompt(prompt_in: PromptIn,  db: Session = Depends(get_db)):
    prompt = Prompt(title=prompt_in.title, done=False)
    db.add(prompt)
    db.commit()
    prompt = get_prompt(db, prompt.id)
    return prompt

# promptを更新
@app.put("/prompts/{prompt_id}")
async def update_prompt(prompt_id: int, prompt_in: PromptIn, db: Session = Depends(get_db)):
    prompt = get_prompt(db, prompt_id)
    prompt.title = prompt_in.title
    prompt.done = prompt_in.done
    db.commit()
    prompt = get_prompt(db, prompt_id)
    return prompt

# promptを削除
@app.delete("/prompts/{prompt_id}")
async def delete_prompt(prompt_id: int, db: Session = Depends(get_db)):
    prompt = get_prompt(db, prompt_id)
    db.delete(prompt)
    db.commit()

# リクエストの度に呼ばれるミドルウェア DB接続用のセッションインスタンスを作成
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response