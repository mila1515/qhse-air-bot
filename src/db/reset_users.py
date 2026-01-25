from src.db.session import engine
from sqlalchemy import text

def reset_users_table():
    print("Dropping users table...")
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS users CASCADE;"))
        conn.commit()
    print("Table users dropped.")

if __name__ == "__main__":
    reset_users_table()
