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
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": str(e)}), 404

@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
