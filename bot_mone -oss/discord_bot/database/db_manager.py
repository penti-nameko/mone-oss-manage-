import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base

DB_URL = os.getenv('DB_URL')
if not DB_URL:
    raise ValueError('DB_URL is not set. 例: sqlite:///database.db')
engine = create_engine(DB_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

# DB初期化
def init_db():
    Base.metadata.create_all(bind=engine)

# セッション取得
def get_session():
    return SessionLocal()

# 例: ギルド追加
def add_guild(guild_id, name, owner_id):
    from database.models import Guild
    session = get_session()
    g = Guild(id=guild_id, name=name, owner_id=owner_id)
    session.add(g)
    session.commit()
    session.close()

# 例: 設定取得
def get_guild_settings(guild_id):
    from database.models import Setting
    session = get_session()
    settings = session.query(Setting).filter_by(guild_id=guild_id).all()
    session.close()
    return {s.key: s.value for s in settings}

def get_guilds():
    """ギルド一覧のダミー取得関数"""
    # 実際はDBから取得
    return [
        {'id': 1, 'name': 'Guild One'},
        {'id': 2, 'name': 'Guild Two'}
    ]

def get_guild_details(guild_id):
    """ギルド詳細のダミー取得関数"""
    # 実際はDBから取得
    return {'id': guild_id, 'name': f'Guild {guild_id}', 'members': 42}