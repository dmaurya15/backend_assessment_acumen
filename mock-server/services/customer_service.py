import json
from typing import List, Dict, Optional


class CustomerService:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.customers = self._load_data()

    def _load_data(self) -> List[Dict]:
        with open(self.file_path, "r") as f:
            return json.load(f)

    def get_customers(self, page: int, limit: int) -> Dict:
        start = (page - 1) * limit
        end = start + limit

        return {
            "data": self.customers[start:end],
            "total": len(self.customers),
            "page": page,
            "limit": limit
        }

    def get_customer_by_id(self, customer_id: str) -> Optional[Dict]:
        return next(
            (c for c in self.customers if c["customer_id"] == customer_id),
            None
        )