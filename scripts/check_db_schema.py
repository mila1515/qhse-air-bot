import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.db.session import engine
from sqlalchemy import inspect

inspector = inspect(engine)
columns = [col['name'] for col in inspector.get_columns('conversations')]
print(f"Columns in 'conversations': {columns}")

columns_users = [col['name'] for col in inspector.get_columns('users')]
print(f"Columns in 'users': {columns_users}")

columns_msgs = [col['name'] for col in inspector.get_columns('messages')]
print(f"Columns in 'messages': {columns_msgs}")
