import pandas as pd
from sqlalchemy import create_engine, text

db_uri = 'mysql+pymysql://newuser:newpassword@localhost:3306/think41'
engine = create_engine(db_uri)

df = pd.read_csv('products.csv')

with engine.begin() as conn:
    # Step 1: Load all departments into a dict {name: id}
    res = conn.execute(text("SELECT id, name FROM departments"))
    dept_map = {row['name']: row['id'] for row in res.mappings()}

    # Step 2: Prepare list of (dept_id, sku) tuples for updating
    updates = []
    for idx, row in df.iterrows():
        dept_name = str(row['department']).strip()
        sku = str(row['sku']).strip()
        if dept_name in dept_map:
            updates.append((dept_map[dept_name], sku))

    # Step 3: Batch update products.department_id by sku
    # This uses executemany to run one UPDATE with many parameters efficiently.
    update_sql = text("UPDATE products SET department_id = :dept_id WHERE sku = :sku")
    conn.execute(update_sql, [{'dept_id': dept_id, 'sku': sku} for dept_id, sku in updates])
