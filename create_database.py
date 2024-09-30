# /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'asakura hiroto'
__version__ = '1.0.0'
__date__ = '2024/09/30 (Created: 2024/09/30)'

from sqlalchemy import Boolean, Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URI = 'sqlite:///./test.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URI, connect_args={'check_same_thread': False}, echo=True
)

Base = declarative_base()

# テーブルの定義
class Prompt(Base):
    __tablename__ = 'prompts'
    # お客様情報
    user_id = Column('user_id', Integer, primary_key = True)

    # 会社名
    company_name = Column('company_name', String(100))

    # 契約状態
    # contract_status = Column('contract_status', Boolean, default=False)

    # ロゴ画像
    logo_image = Column('logo_image', String(500))

    # ホームページの文章
    # homepage_text = Column('homepage_text', String(1000))

    # 会社やお客様の説明
    # company_description = Column('company_description', String(1000))

    # 商品のサービスや説明
    # product_service_description = Column('product_service_description', String(1000))

    # 商品やサービスの価格
    # product_service_price = Column('product_service_price', String(200))

    # 商品やサービスの画像
    # product_service_image = Column('product_service_image', String(500))

    # 会社説明
    # company_info = Column('company_info', String(1000))

    # 実績の紹介（画像）
    # achievement_image = Column('achievement_image', String(500))

    # 実績の紹介（文字）
    # achievement_text = Column('achievement_text', String(1000))

    # 会社情報（住所・電話番号・営業時間・営業時間・アクセス）
    # company_details = Column('company_details', String(1000))

    # 予約フォーム・求人掲載リンク
    # reservation_recruitment_link = Column('reservation_recruitment_link', String(500))

    # SNSリンク
    # sns_links = Column('sns_links', String(500))

    # webページのカラー
    # webpage_color = Column('webpage_color', String(50))

# テーブル作成
Base.metadata.create_all(bind=engine)


