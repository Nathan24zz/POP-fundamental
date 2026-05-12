from fastapi import FastAPI
from model import Product
from database import session, engine
import database_model

# ----- DATABASE -----
# make all tables that are mention in database model
database_model.Base.metadata.create_all(bind=engine)

# usually we are not doing this in real application
# make data to initialize database
products = [
    Product(id=1, name="Phone", description="A smartphone", price=699.9, quantity=50),
    Product(id=2, name="Laptop", description="A powerful laptop", price=999.9, quantity=30),
]

# populate db for the first time
def init_db():
    db = session()

    # To get how many rows in the database
    # SELECT COUNT(*) FROM product
    count = db.query(database_model.Product).count

    if count == 0:
        for product in products:
            # first, convert pydantic model --> SQLAlchemy model
            # model_dump() is method for converting a Pydantic model instance into a standard Python dictionary
            # the double asterisk (**) is the dictionary unpacking operator
            db.add(database_model.Product(**product.model_dump()))

    # to save permanently
    db.commit()

init_db()
# ----- DATABASE -----

app = FastAPI()

# ----- API -----
# home page
@app.get("/")
def greet():
    return "Welcome to World"

# show all products
@app.get("/products")
def get_all_products():
    return products

# get specific product
@app.get("/product/{id}")
def get_product_by_id(id: int):
    for product in products:
        if product.id == id:
            return product
    
    return "Products not found"

# add product
@app.post("/product")
def add_product(product: Product):
    # hint in argument is for FastAPI testing 
    products.append(product)
    return product

# update product
@app.put("/product")
def update_product(id: int, product: Product):
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return "Product Updated"

    return "Products not found"

# delete product
@app.delete("/product")
def delete_product(id: int):
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]
            return "Product Deleted"

    return "Products not found"
# ----- API -----