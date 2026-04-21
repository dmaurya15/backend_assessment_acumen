from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Load JSON once
with open("data/customers.json") as f:
    customers = json.load(f)


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/api/customers", methods=["GET"])
def get_customers():
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
    except ValueError:
        return jsonify({"error": "Invalid pagination"}), 400

    start = (page - 1) * limit
    end = start + limit

    return jsonify({
        "data": customers[start:end],
        "total": len(customers),
        "page": page,
        "limit": limit
    })


@app.route("/api/customers/<customer_id>", methods=["GET"])
def get_customer(customer_id):
    customer = next((c for c in customers if c["customer_id"] == customer_id), None)

    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    return jsonify(customer)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)