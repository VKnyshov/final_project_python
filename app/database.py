import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}"

# Чекаємо, поки MySQL стане доступним
for _ in range(10):  # 10 спроб з інтервалом у 3 секунди
    try:
        engine = create_engine(DATABASE_URL)
        connection = engine.connect()
        connection.close()
        print("✅ MySQL підключено!")
        break
    except Exception as e:
        print(f"❌ MySQL не відповідає, чекаємо... ({e})")
        time.sleep(3)
else:
    raise Exception("❌ Неможливо підключитися до MySQL!")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
