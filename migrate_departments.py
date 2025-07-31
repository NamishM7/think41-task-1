import pandas as pd
from sqlalchemy import create_engine

db_uri = 'mysql+pymysql://newuser:newpassword@localhost:3306/think41'
engine = create_engine(db_uri)

# Fetch unique department names
df = pd.read_sql('SELECT DISTINCT department FROM products WHERE department IS NOT NULL', engine)
for dept in df['department']:
    engine.execute('INSERT IGNORE INTO departments (name) VALUES (%s)', (dept,))
