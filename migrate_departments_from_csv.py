import pandas as pd
from sqlalchemy import create_engine, text

db_uri = 'mysql+pymysql://newuser:newpassword@localhost:3306/think41'
engine = create_engine(db_uri)

df = pd.read_csv('products.csv')

with engine.begin() as conn:  # ensures transaction is committed
    for dept in df['department'].dropna().unique():
        dept_str = str(dept).strip()
        if dept_str:
            conn.execute(text("INSERT IGNORE INTO departments (name) VALUES (:dept_name)"), {'dept_name': dept_str})
print("Department column unique values:", df['department'].dropna().unique())
