# Clue Insights Backend Technical Assessment 

## Introduction

This project contains code implementing a RESTful API for managing user subscriptions.

## Stack
This project is built using Flask(Python web framework), MySQL(database) and SQLAlchemy(Object Relational Mapper).

## Setup

Setting up this project is simple as it has already been configured using docker and docker-compose(dockerized). All you need is to carry out the following steps accordingly.

### 1. Clone github repository
```bash
git clone https://github.com/el-caminoo/Clue-Insights
```
### 2. Build the application

Make sure you have docker and docker compose installed on your computer then run
```bash
docker compose build
```
to build the application components.

### 3. Run the application
After successfully building, we can run the containers using the following command
```bash
docker compose up
```

## OpenAPI Specification
The OpenAPI Specification documentation can be found at http://127.0.0.1:8000/doc/

## API Endpoints 
| URL      | Description | Remark  |
|----------|-------------|---------|
| http://localhost:8000/user/create | This endpoint creates a staff account with admin role in order to create products(subscription plans on the platform) | No JWT required
| http://localhost:8000/user/login  | This endpoint logs in a staff account with admin role to obtain a JWT used to create products | No JWT required 
| http://localhost:8000/customer/create | This endpoint creates a customer that potentially purchases, upgrades or cancels a subscription plan | No JWT required  
| http://localhost:8000/customer/login | This endpoint logs in a customer in order to obtain a JWT to make customer based request | No JWT required
| http://localhost:8000/product/create | This endpoint is used by a staff account with an "admin" role to create products(subscription plans) | JWT required
| http://localhost:8000/product/list | This endpoint returns a list of subscription plans available for purchase | No JWT required
| http://localhost:8000/subscription/purchase | This endpoint is used by a customer to purchase a subscription plan | JWT required
| http://localhost:8000/subscription/upgrade | This endpoint is used by a customer to upgrade to a new subscription plan | JWT required
| http://localhost:8000/subscription/cancel | This endpoint is used to cancel a customer's active subscription plan | JWT required
| http://localhost:8000/subscription/active/all | Returns all active subscriptions | No JWT required
| http://localhost:8000/subscription/list | Returns a list of subscriptions in descending order of its start_at column | No JWT required
| http://localhost:8000/subscription/customer/history | Returns the subscription history of a customer | JWT required


## Alternative setup
The project can also be setup by creating a virtual environment on your computer and installing the project dependencies using the Pip tool.

### 1. Create a python virtual environment
```bash
python3 -m venv [name of virtual environment folder]
```
This can be done in the base directory of the cloned repository.
### 2. Activated the virtual environment
This can be done by running the following command
```bash
source [virtial environment folder]/bin/activate
```

### 3. Install project dependencies
This can be done by running the following command
```bash
pip install -r requirements.txt
```
in the base directory or where the requirements.txt file is located.
### 4. Setting up your database
This project is configured to work with a MySQL database but can also work with a SQlite DB. Make sure to specify what database you intend to make use of in your .env file.

### 5. Environmental Variables
Ensure you have the values of the following variables in your .env file for the project to work correctly

* FLASK_APP=[your value]
* FLASK_ENV=[your value]
* DATABASE_URL=[your mysql or sqlite db url e.g 'mysql+mysqlconnector://[username]:[password]@localhost/[db-name]']
* SECRET_KEY=[your value]
* JWT_SECRET_KEY=[your value]
### 6. Running the project
The project can be started by running the following command
```bash
gunicorn wsgi:app 
```
### 7. Run database migrations
It is important to run migrations to the database before any testing can begin. This can be done by running the following command
```bash
flask db upgrade
```
### 8. Seeding the database
The project contains a seed.py file that inserts requisite data into the database used to effectively carry out testing of the APIs. It is important you run the following command before you begin testing
```bash
python seed.py
```
The folder also contains a doc.txt file that contains details and explainations about the project.

Everything should work perfectly if all the steps are followed correctly.

## Testing

In order to run unit tests, run the following command from the root directory of the project
```bash
pytest
```