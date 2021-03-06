# Store Manager

Store Manager is a restful api that helps store owners manage sales and product inventory records. This application is 
meant for use in a single store.

[![codecov](https://codecov.io/gh/fahadmak/store_manager_api/branch/develop/graph/badge.svg)](https://codecov.io/gh/fahadmak/store_manager_api)
[![Coverage Status](https://coveralls.io/repos/github/fahadmak/store_challenge_3/badge.svg?branch=develop)](https://coveralls.io/github/fahadmak/store_challenge_3?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/31f1ccb43fa804d72b7f/maintainability)](https://codeclimate.com/github/fahadmak/store_challenge_3/maintainability)
[![Build Status](https://travis-ci.org/fahadmak/store_challenge_3.svg?branch=develop)](https://travis-ci.org/fahadmak/store_challenge_3)

**Features of the Application**

* Adding Products
* Viewing all products
* Delete a Product
* Modify a Product
* Creating a Sale Record
* Viewing Sale Records
* Creates a category for Products
* Delete a Category
* Modify a Category
* Views a Category

As a store attendant/admin:

* Can get all products
* Can get a specific product
* Can add a sale order
* Views a Category

As User:

* Can add a product
* Can get all sale order records
* Create User
* Assign Admin rights
* Login / Log out

As admin:

* Can add a product
* Can get all sale order records
* Creates a category for Products
* Delete a Category
* Modify a Category

**App Documenation**

To learn more about the application try the app documenatation found on https://storemanager18.docs.apiary.io/#

**Demo**

To use the application via postman go to

`https://store-challenge-3-api.herokuapp.com/api/v1`

Use the following endpoints:

 EndPoint                         | Functionality
------------------------          | ----------------------
POST /auth/login                  | Login
POST /auth/signup                 | Create User
PUT /auth/promote/<user_id>       | Give Admin rights
POST /products                    | Add a new product
PUT /product/<product_id>         | Modify a Product
GET /products                     | Gets all products
GET /products/<product_id>        | Gets a product
DELETE /products/<product_id>     | Delete a product
POST /sales                       | Add a new sale record
GET /sales                        | Gets all sale records
GET /sales/<sale_id>              | Gets a sale
POST /categories                  | Add a category
GET /categories/<category_id>     | Gets a product
PUT /categories/<category_id>     | Modify a category
DELETE /categories/<category_id>  | Delete a category


**Prerequisites used to build the application**

* Python 3.6.5

* Flask

**Installation**

I. Initialize git in a new directory. Clone this repository by running in that new directory

`$ git clone https://github.com/fahadmak/store_challenge_3.git`

II.  Create a virtual environment. For example, with virtualenv, create a virtual environment named venv using

`$ virtualenv venv`

III. Activate the virtual environment

`$ cd venv/scripts/activate`

IV. Install the dependencies in the requirements.txt file using pip

`$ pip install -r requirements.txt`

V. Start the application

`$ python app.py`

