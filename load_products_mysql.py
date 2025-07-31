import pandas as pd
from sqlalchemy import create_engine

csv_path = 'products.csv'
db_uri = 'mysql+pymysql://newuser:newpassword@localhost:3306/think41'  # Edit credentials

df = pd.read_csv(csv_path)
engine = create_engine(db_uri)
df.to_sql('products', con=engine, if_exists='append', index=False)
