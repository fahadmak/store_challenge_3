
#Store Manager

Store Manager is a restful api that helps store owners manage sales and product inventory records. This application is 
meant for use in a single store.

[![codecov](https://codecov.io/gh/fahadmak/store_manager_api/branch/develop/graph/badge.svg)](https://codecov.io/gh/fahadmak/store_manager_api)
[![Coverage Status](https://coveralls.io/repos/github/fahadmak/store_manager_api/badge.svg?branch=develop)](https://coveralls.io/github/fahadmak/store_manager_api?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/6b72aeef25fc7604088b/maintainability)](https://codeclimate.com/github/fahadmak/store_manager_api/maintainability)
[![Build Status](https://travis-ci.org/fahadmak/store_manager_api.svg?branch=develop)](https://travis-ci.org/fahadmak/store_manager_api)

**Features of the Application**

* Adding Products
* Viewing all products
* Creating a Sale Record
* Viewing Sale Records

As a store attendant/admin:

* Can get all products
* Can get a specific product
* Can add a sale order

As admin:

* Can add a product
* Can get all sale order records

**Demo**

To use the application via postman go to

`https://api-stores-heroku.herokuapp.com/api/v1`

Use the following endpoints:

 EndPoint                       | Functionality
------------------------        | ----------------------
POST /products                  | Add a new product
GET /products                   | Gets all products
GET /products/<product_id>      | Gets a product
POST /sales                     | Add a new sale record
GET /sales                      | Gets all sale records
GET /sales/<sale_id>            | Gets a product


**Prerequisites used to build the application**

* Python 3.6.5

* Flask

**Installation**

I. Initialize git in a new directory. Clone this repository by running in that new directory

`$ git clone https://github.com/fahadmak/store_manager_api.git`

II.  Create a virtual environment. For example, with virtualenv, create a virtual environment named venv using

`$ virtualenv venv`

III. Activate the virtual environment

`$ cd venv/scripts/activate`

IV. Install the dependencies in the requirements.txt file using pip

`$ pip install -r requirements.txt`

V. Start the application

`$ python app.py`

