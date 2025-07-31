from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from sqlalchemy import create_engine, text

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains (customize as needed)

# Update with your credentials
DATABASE_URI = 'mysql+pymysql://newuser:newpassword@localhost:3306/think41'
engine = create_engine(DATABASE_URI)
@app.route('/api/products', methods=['GET'])
def get_products():
    # Pagination parameters with defaults
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    offset = (page - 1) * per_page

    with engine.connect() as conn:
        query = text("""
            SELECT p.*, d.name AS department_name
            FROM products p
            LEFT JOIN departments d ON p.department_id = d.id
            LIMIT :limit OFFSET :offset
        """)
        result = conn.execute(query, {"limit": per_page, "offset": offset})

        # Convert results to list of dicts, including department_name
        products = [dict(zip(result.keys(), row)) for row in result]

    return jsonify(products)


@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    with engine.connect() as conn:
        query = text("""
            SELECT p.*, d.name AS department_name
            FROM products p
            LEFT JOIN departments d ON p.department_id = d.id
            WHERE p.id = :id
        """)
        result = conn.execute(query, {"id": product_id})
        row = result.fetchone()

        if row is None:
            abort(404, description="Product not found")

        return jsonify(dict(zip(result.keys(), row)))
@app.route('/api/departments', methods=['GET'])
def list_departments():
    with engine.begin() as conn:
        query = text("""
            SELECT d.id, d.name, COUNT(p.id) AS product_count
            FROM departments d
            LEFT JOIN products p ON p.department_id = d.id
            GROUP BY d.id, d.name
        """)
        result = conn.execute(query)
        departments = [dict(zip(result.keys(), row)) for row in result]
    return jsonify({"departments": departments})

@app.route('/api/departments/<int:dept_id>', methods=['GET'])
def get_department(dept_id):
    with engine.begin() as conn:
        query = text("SELECT id, name FROM departments WHERE id = :id")
        result = conn.execute(query, {"id": dept_id})
        row = result.fetchone()
        if row is None:
            abort(404, description="Department not found")
        department = dict(zip(result.keys(), row))
    return jsonify(department)

@app.route('/api/departments/<int:dept_id>/products', methods=['GET'])
def get_department_products(dept_id):
    with engine.begin() as conn:
        # Get department name
        d_result = conn.execute(text("SELECT name FROM departments WHERE id = :id"), {"id": dept_id})
        d_row = d_result.fetchone()
        if d_row is None:
            abort(404, description="Department not found")
        dept_name = d_row[0]

        # Get products
        p_query = text("""
            SELECT p.*, d.name AS department_name
            FROM products p
            JOIN departments d ON p.department_id = d.id
            WHERE d.id = :id
        """)
        p_result = conn.execute(p_query, {"id": dept_id})
        products = [dict(zip(p_result.keys(), row)) for row in p_result]

    return jsonify({
        "department": dept_name,
        "products": products
    })

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": str(e)}), 404

@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
