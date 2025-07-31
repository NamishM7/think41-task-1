import pandas as pd
from sqlalchemy import create_engine

db_uri = 'mysql+pymysql://newuser:newpassword@localhost:3306/think41'  # Edit credentials
engine = create_engine(db_uri)
result = pd.read_sql('SELECT * FROM products LIMIT 10;', engine)
print(result)
