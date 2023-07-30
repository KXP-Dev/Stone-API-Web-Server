# T2A2 - API Webserver Project Kim Perez

## R1	Identification of the problem you are trying to solve by building this particular app.

I'm trying to solve the main problem a small business would eventually reach when their business is rapidly growing, they are managing more employees, handling more stock and getting an increased intake of customers. Most small businesses would have started with a manual paper based system, which would be perfectly fine for a much smaller business just starting out but eventually a transition to a relational database system would be incredibly beneficial to the business' growth. I've designed my web API and database specifically for a stonemason business that stocks and sells stone materials.

## R2	Why is it a problem that needs solving?

If the business keeps using a manual paper based system whilst expecting business growth then the business will run into many problems. Handling a warehouse with thousands of stock materials and products would easily overwhelm a business that hasn't transitioned. If the business hires more employees it would be difficult to manage them, their employee accounts and employee authorisation and priviliges. With business growth comes more customers and orders. Using the app the business will be able to efficiently and easily manage their orders, employees, customers and stock whilst allowing for upscalability and data security for the business.

## R3	Why have you chosen this database system. What are the drawbacks compared to others?

## R4	Identify and discuss the key functionalities and benefits of an ORM

## R5	Document all endpoints for your API

Register new employee:
POST
localhost:8080/auth/register
Body - raw - JSON
{
  "employee_name": "John Doe",
  "employee_email": "johndoe@email.com",
  "password": "password123"
}
{
    "employee_email": "rickgrimes@email.com",
    "employee_id": 5,
    "employee_name": "Rick Grimes",
    "is_admin": false
}

Employee login:
POST
localhost:8080/auth/login
{
    "employee_email": "kimperez@admin.com",
    "password": "adminpw"
}
{
    "employee_email": "kimperez@admin.com",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5MDY4NzcwMywianRpIjoiYzVmZmJmMDMtNDQwYy00YzI2LTk5NTMtNjUxN2QwZjlhY2Q5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE2OTA2ODc3MDMsImV4cCI6MTY5MDc3NDEwM30.bl6ZNVwRR03uc6WzNT6-qjcMAZaeChrmkWf-NMahdu4"
}

Check admin:
POST
localhost:8080/auth/check-admin
Admin access token
{
    "message": "User is an admin"
}

Delete employee:
DELETE
localhost:8080/auth/delete/5
Admin access token
{
    "message": "Employee deleted successfully"
}

Update employee:
PUT
localhost:8080/auth/update/4
Admin access token
{
  "employee_name": "Kaiser Perez",
  "employee_email": "kaiserperez1@email.com",
  "is_admin": true
}
{
    "message": "Employee information updated successfully"
}

All employees:
GET
localhost:8080/auth/employees
Admin access token
{
    "employees": List of all employees
}


Create stock:
POST
localhost:8080/inventory/create
Admin access token
{
    "product_name": "Carara Marble",
    "quantity": 35,
    "unit_price": 1100
}
{
    "inventory_item": {
        "product_id": 3,
        "product_name": "Carara Marble",
        "quantity": 35,
        "unit_price": 1100.0
    },
    "message": "Inventory item created successfully"
}

DELETE stock item"
DELETE
localhost:8080/inventory/delete/3
Admin access token
{
    "message": "Inventory item deleted successfully"
}

Update stock item:
PUT
localhost:8080/inventory/update
Access token
{
  "product_id": 1,
  "product_name": "Calacatta Marble",
  "quantity": 60,
  "unit_price": 2000
}
{
    "inventory_item": {
        "product_id": 1,
        "product_name": "Calacatta Marble",
        "quantity": 60,
        "unit_price": 2000.0
    },
    "message": "Inventory item updated successfully"
}

Get all stock:
GET
localhost:8080/inventory/all
{
    "inventory_items": [
        {
            "product_id": 2,
            "product_name": "Black Granite",
            "quantity": 50,
            "unit_price": 1000.0
        },
        {
            "product_id": 1,
            "product_name": "Calacatta Marble",
            "quantity": 60,
            "unit_price": 2000.0
        }
    ]
}

Create Customer:
POST
localhost:8080/customers/create
Admin access token
{
  "customer_number": "0000000003",
  "customer_name": "John Smith",
  "email": "johnsmith@email.com",
  "address": "125 Melbourne Street"
}
{
    "customer": {
        "address": "125 Melbourne Street",
        "customer_id": 3,
        "customer_name": "John Smith",
        "customer_number": "0000000003",
        "email": "johnsmith@email.com"
    },
    "message": "Customer created successfully"
}

Delete Customer:
DELETE
localhost:8080/customers/delete/3
Admin access token
{
    "message": "Customer deleted successfully"
}

Get Customer Info:
GET
localhost:8080/customers/1
Access token
{
    "customer": {
        "address": "122 Main Street",
        "customer_id": 1,
        "customer_name": "Mariah Carey",
        "customer_number": "0000000000",
        "email": "mariahcarey1@email.com"
    }
}

Update Customer:
PUT
http://localhost:8080/customers/update/1
Access Token
{
  "customer_name": "Mariah Carey",
  "address": "122 Main Street",
  "email": "mariahcarey1@email.com",
  "customer_number": "0000000000"
}
{
    "customer": {
        "address": "122 Main Street",
        "customer_id": 1,
        "customer_name": "Mariah Carey",
        "customer_number": "0000000000",
        "email": "mariahcarey1@email.com"
    },
    "message": "Customer updated successfully"
}

Get all customers:
GET
localhost:8080/customers/all
Access Token
{
    "customers": [
        {
            "address": "125 Sydney Street",
            "customer_id": 2,
            "customer_name": "Jane Smith",
            "customer_number": "0000000002",
            "email": "janesmith@email.com"
        },
        {
            "address": "122 Main Street",
            "customer_id": 1,
            "customer_name": "Mariah Carey",
            "customer_number": "0000000000",
            "email": "mariahcarey1@email.com"
        }
    ]
}

Create order:
POST
http://localhost:8080/orders/create
Admin access token
{
  "customer_id": 2,
  "total_amount": 7000
}
{
    "message": "Order created successfully",
    "order": {
        "customer_id": 2,
        "order_id": 5,
        "total_amount": 7000.0
    }
}

Get all orders:
GET
localhost:8080/orders/all
Access Token
{
    "orders": [
        {
            "customer_id": 2,
            "order_id": 1,
            "total_amount": 4000.0
        },
        {
            "customer_id": 1,
            "order_id": 2,
            "total_amount": 6000.0
        },
        {
            "customer_id": 2,
            "order_id": 3,
            "total_amount": 9000.0
        },
        {
            "customer_id": 1,
            "order_id": 4,
            "total_amount": 8000.0
        },
        {
            "customer_id": 2,
            "order_id": 5,
            "total_amount": 7000.0
        }
    ]
}

Delete order:
DELETE
localhost:8080/orders/delete/5
Admin access token
{
    "message": "Order deleted successfully"
}

Update order:
PUT
localhost:8080/orders/update/4
Access token
{
    "total_amount": 8200
}
{
    "message": "Order updated successfully",
    "order": {
        "customer_id": 1,
        "order_id": 4,
        "total_amount": 8200.0
    }
}
## R6	An ERD for your app

## R7	Detail any third party services that your app will use

## R8	Describe your projects models in terms of the relationships they have with each other

## R9	Discuss the database relations to be implemented in your application

## R10	Describe the way tasks are allocated and tracked in your project