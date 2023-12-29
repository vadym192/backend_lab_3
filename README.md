---

## Lab Variant: 16%3=1
Currencies
--- 

# Flask Currency Management API

## Overview
This Flask API provides a simple yet powerful system for managing currencies, users, and transactions. It supports CRUD operations for each entity and is designed to be easy to use and integrate into any front-end application.

## Features
- **Currency Management**: Add, view, update, and delete currency data.
- **User Management**: Create, retrieve, and update user information, including default currencies.
- **Transaction Handling**: Record and retrieve transaction details.

## Getting Started

### Prerequisites
- Python 3.8+
- Flask
- PostgreSQL
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Marshmallow

### Installation
1. Clone the repository:
   ```bash
   git clone [repository-url]
   ```
2. Navigate to the project directory:
   ```bash
   cd [project-name]
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your PostgreSQL database and update the connection string in `app.config['SQLALCHEMY_DATABASE_URI']`.

5. Run the migrations:
   ```bash
   flask db upgrade
   ```

### Running the Application
1. Build the Docker image:
   ```bash
   docker-compose build
   ```
2. Run the application:
    ```bash
   docker-compose up
   ```
   The API will be available at `http://localhost:3000` by default.

## API Endpoints

### Currencies
- POST `/currencies`: Add a new currency.
- GET `/currencies`: Retrieve all currencies.
- GET `/currencies/<currency_id>`: Retrieve a specific currency.
- PUT `/currencies/<currency_id>`: Update a specific currency.
- DELETE `/currencies/<currency_id>`: Delete a specific currency.

### Users
- POST `/users`: Create a new user.
- GET `/users`: Retrieve all users.
- PUT `/users/<user_id>`: Update a specific user.

### Transactions
- POST `/transactions`: Add a new transaction.
- GET `/transactions`: Retrieve all transactions.
- GET `/transactions/<transaction_id>`: Retrieve a specific transaction.

## Usage
To use the API, send HTTP requests to the specified endpoints with the required JSON payload.

### Example Request
```json
POST /users
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john.doe@example.com",
  "default_currency_id": 1
}
```
