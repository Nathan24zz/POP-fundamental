from fastapi import FastAPI, Depends
from model import Product
from sqlalchemy.orm import Session
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

# create connection once, waiting other function do the query, then close
def get_db():
    db = session()

    # try: Wraps the "risky" code that might cause an error.
    try:
        # waiting for other function to use it
        yield db
    # finally: Contains "cleanup" code that always executes, even if an error occurs or the program returns early
    finally:
        db.close()

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
# Dependency injection (inject db variable from get_db())
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(database_model.Product).all()
    return db_products

# get specific product
@app.get("/product/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    # if get product > 1, return the first one
    db_product = db.query(database_model.Product).filter(database_model.Product.id == id).first()
    if db_product:
        return db_product
    
    return "Product not found"

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