import requests
import dlt
from sqlalchemy.orm import Session
from models.customers import Customer
from datetime import datetime


FLASK_URL = "http://mock-server:5000/api/customers"


def fetch_all_customers():
    page = 1
    limit = 10
    all_customers = []

    while True:
        response = requests.get(f"{FLASK_URL}?page={page}&limit={limit}")
        data = response.json()

        customers = data.get("data", [])

        if not customers:
            break

        all_customers.extend(customers)

        if len(customers) < limit:
            break

        page += 1

    return all_customers


# Minimal dlt resource (just for compliance)
@dlt.resource(name="customers")
def customer_resource():
    return fetch_all_customers()


def upsert_customers(db: Session, customers):
    for c in customers:
        # convert types
        c["date_of_birth"] = datetime.strptime(c["date_of_birth"], "%Y-%m-%d").date()
        c["created_at"] = datetime.fromisoformat(c["created_at"])

        existing = db.query(Customer).filter_by(customer_id=c["customer_id"]).first()

        if existing:
            for key, value in c.items():
                setattr(existing, key, value)
        else:
            db.add(Customer(**c))

    db.commit()