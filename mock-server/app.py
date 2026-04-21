from flask import Flask, jsonify, request
from services.customer_service import CustomerService

app = Flask(__name__)

customer_service = CustomerService("data/customers.json")


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Flask Mock Server Running"}), 200


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/api/customers", methods=["GET"])
def get_customers():
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))

        if page < 1 or limit < 1:
            raise ValueError

    except ValueError:
        return jsonify({"error": "Invalid pagination parameters"}), 400

    result = customer_service.get_customers(page, limit)
    return jsonify(result), 200


@app.route("/api/customers/<customer_id>", methods=["GET"])
def get_customer(customer_id):
    customer = customer_service.get_customer_by_id(customer_id)

    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    return jsonify(customer), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)