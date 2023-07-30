# T2A2 - API Webserver Project Kim Perez

## R1	Identification of the problem you are trying to solve by building this particular app.

I'm trying to solve the main problem a small business would eventually reach when their business is rapidly growing, they are managing more employees, handling more stock and getting an increased intake of customers. Most small businesses would have started with a manual paper based system, which would be perfectly fine for a much smaller business just starting out but eventually a transition to a relational database system would be incredibly beneficial to the business' growth. I've designed my web API and database specifically for a stonemason business that stocks and sells stone materials.

## R2	Why is it a problem that needs solving?

If the business keeps using a manual paper based system whilst expecting business growth then the business will run into many problems. Handling a warehouse with thousands of stock materials and products would easily overwhelm a business that hasn't transitioned. If the business hires more employees it would be difficult to manage them, their employee accounts and employee authorisation and priviliges. With business growth comes more customers and orders. Using the app the business will be able to efficiently and easily manage their orders, employees, customers and stock whilst allowing for upscalability and data security for the business.

## R3	Why have you chosen this database system. What are the drawbacks compared to others?

I have chosen PostgreSQL as my database system because it is an open source relational database which makes it free for access and have a large community that help develop, contribute and improve the software. PostgreSQL also has robust features, reliability, and performance. PostgreSQL is known for its ability to handle complex queries, support for advanced data types, and its ACID-compliant transactions, making it suitable for data-intensive applications. Additionally, PostgreSQL is an open-source database, providing cost-effectiveness and large community for support and continuous improvement. However, some drawbacks compared to other systems like MySQL and MongoDB include slightly higher complexity in setup and administration, and while it excels in handling structured data, NoSQL databases like MongoDB may perform better with unstructured data and high scalability requirements. Main reasons why i chose PostgreSQL is because it is open source and the capabilities of the database is more than enough for my project.

## R4	Identify and discuss the key functionalities and benefits of an ORM

An Object-Relational Mapping (ORM) is a technique that helps developers work with databases using familiar object-oriented code. It takes away the difficulties of writing database queries, allowing developers to interact with the database as if it were a collection of objects. The benefits of using an ORM include easier data validation, compatibility with different platforms, simplified relationships between data, and faster development. There might be some trade offs in terms of performance and memory usage. Overall, ORM is a powerful tool that makes database interactions simpler and more efficient for developers.

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

![My ERD](images\api_erd.jpg)

## R7	Detail any third party services that your app will use

Flask: Flask is a 3rd party framework for Python. It provides tools and components to build web applications such as routing, request handling and response rendering. Flask is used to create my endpoints as well as the Blueprint functionality.

SQLAlchemy: SQLAlchemy is an ORM library that is used to simplify database interactions in Python. This eliminates the need to write raw SQL queries and instead using Python objects.

FLask-JWT-Extended: Is an extension for Flask that enables JWT based authentication and authorisation which also allows me to use access tokens to set up the authentication and access control of my API.

Flask-Bcrypt: Is an extension for Flask that provides tools for hashing and encrypting passwords. This is used to securely store user passwords in the database.

Marshmallow: Marshmallow is a library for object serialisation and deserialisation in Python. It helps convert complex data types like models into JSON or other formats when sending responses to employees.

Postman: Postman is a API development tool that I used to design, test and document my APIs.

## R8	Describe your projects models in terms of the relationships they have with each other

Customer Table -
Primary Key: 'customer_id'
Attributes: customer_id, customer_number, customer_name, email, and address.
This table represents individual customers and their information. It has a one-to-many relationship with the 'order' table.
One 'customer' can have multiple orders associated with them.

Order Table -
Primary Key: 'order_id'
Attributes: order_id, customer_id, and total_amount.
This table represents individual orders and their information in the database. It has a many-to-one relationship with the 'customer' table.
Each 'Order' is associated with one specific 'Customer'

Employee Table -
Primary Key: 'employee_id'
Attributes: employee_id, employee_email, employee_name, password, is_admin

Stock Table -
Primary Key: 'product_id'
Attributes: product_id, product_name, quantity, unit_price.

## R9	Discuss the database relations to be implemented in your application

I only have 1 database relation in my project and that is between customers and orders. I have implemented this relation by defining my order model by including a Foreign Key column that references customer id column in the customer table. I then defined the customer model with with 'backref' parameter to create a reverse reference from customer to order. Using 'relationship' allowed me to establish this link between my models. I was also planning to make a relation between stock and order for allocating stock when creating orders but I didn't have enough time.

## R10	Describe the way tasks are allocated and tracked in your project

In my project, I used Trello as the tool to manage and keep track of tasks. Trello is a platform where tasks are organised as cards on boards. Each card represents a specific task and includes important details like descriptions and deadlines. I can easily see my tasks and update their progress by moving cards through different lists, such as "To Do," "In Progress," and "Completed."

My Trello Board [My Trello Board](https://trello.com/invite/b/yQPjUT3m/ATTI500d4ea7e4801e4a2e92109c577574b94913EF88/api-webserver).

![My Trello Image](images/trello_board.jpg)