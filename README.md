Backend Data Pipeline System

-> Overview
This pro:ject is a containerized data pipeline system that simulates a real-world ingestion and storage workflow.
It consists of three services:

Flask Mock API → Serves customer data from a JSON source
FastAPI Service → Ingests, processes, and exposes data APIs
PostgreSQL → Persistent storage layer

The system demonstrates data ingestion, pagination handling, upsert logic, and RESTful API design using a microservices architecture.

-> Architecture |
customers.json
     |
Flask Service (Mock Data API - :5000)
     |
FastAPI Service (Ingestion + API Layer - :8000)
     |
PostgreSQL Database (Persistent Storage - :5432)

-> Tech Stack
Python 3.10+
Flask
FastAPI
SQLAlchemy
PostgreSQL 15
dlt (data ingestion framework)
Docker & Docker Compose

-> Project Structure
project-root/
├── docker-compose.yml
├── README.md
│
├── mock-server/
│   ├── app.py
│   ├── data/customers.json
│   ├── requirements.txt
│   └── Dockerfile
│
└── pipeline-service/
    ├── main.py
    ├── database.py
    ├── models/
    │   └── customer.py
    ├── services/
    │   └── ingestion.py
    ├── requirements.txt
    └── Dockerfile

-> Getting Started
1. Clone the repository
git clone <repo-url>
cd project-root
2. Build and run services
docker-compose up --build -d
3. Verify running containers
docker ps

-> API Endpoints
1. Flask Mock Server (Port 5000)
Get Customers (Paginated)
GET /api/customers?page=1&limit=10
Get Customer by ID
GET /api/customers/{id}
Health Check
GET /api/health

Notes:

Data is loaded from customers.json
Pagination is supported via query params
Returns 404 if customer is not found

2. FastAPI Service (Port 8000)
Ingest Data from Flask → PostgreSQL
POST /api/ingest

Description:

Fetches paginated data from Flask API
Processes and upserts records into PostgreSQL

Response:

{
  "status": "success",
  "records_processed": 20
}
Get Customers (Database)
GET /api/customers?page=1&limit=10
Get Customer by ID
GET /api/customers/{id}

3. Database Schema
Table: customers
Column	Type	Constraints
customer_id	VARCHAR(50)	PRIMARY KEY
first_name	VARCHAR(100)	NOT NULL
last_name	VARCHAR(100)	NOT NULL
email	VARCHAR(255)	NOT NULL
phone	VARCHAR(20)	NULL
address	TEXT	NULL
date_of_birth	DATE	NULL
account_balance	DECIMAL(15,2)	NULL
created_at	TIMESTAMP	NULL

4. Data Flow
Flask service reads customer data from JSON file
FastAPI fetches data using paginated requests
Data is processed via ingestion service
Records are upserted into PostgreSQL
FastAPI exposes APIs for querying stored data

5. Key Features
Pagination support across services
Stateless Flask mock API
Upsert-based ingestion (idempotent writes)
Clean separation of services (Flask / FastAPI / DB)
Dockerized environment for consistent setup
Error handling for missing records and invalid requests

6. Testing the System
Start all services
docker-compose up -d
Test Flask API
curl "http://localhost:5000/api/customers?page=1&limit=5"
Trigger ingestion
curl -X POST "http://localhost:8000/api/ingest"
Query FastAPI data
curl "http://localhost:8000/api/customers?page=1&limit=5"

7. Docker Services
Service	Port	Description
postgres	5432	PostgreSQL database
mock-server	5000	Flask mock data API
pipeline-service	8000	FastAPI ingestion service

8. Design Notes
Flask acts purely as a data provider layer
FastAPI handles business logic + ingestion + APIs
PostgreSQL ensures persistent and queryable storage
System is designed to be stateless and horizontally scalable

9. Status

All required components implemented:

 Flask API with pagination
 FastAPI ingestion pipeline
 PostgreSQL integration
 Upsert logic
 Docker Compose orchestration
 End-to-end data flow verified
