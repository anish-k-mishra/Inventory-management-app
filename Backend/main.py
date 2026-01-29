from fastapi import FastAPI
from models import Products
from database import session, engine
import database_models

app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "Welcome to Inventory Manager"

products = [
    Products(id=1, name="Phone", description="Budget phone", price=99, quantity=10),
    Products(id=2, name="Laptop", description="Budget Laptop", price=199, quantity=6),
    Products(id=3, name="Tablet", description="Budget Tablet", price=79, quantity=8),
    Products(id=4, name="Table", description="Budget wooden Table", price=19, quantity=4),
    Products(id=5, name="Pen", description="Budget blue pen", price=5, quantity=7)
]

@app.get("/products")
def get_all_products():
    # db connection 
    db = session()
    return products

@app.get("/product/{id}")
def get_product_by_id(id: int):
    for product in products:
        if(product.id == id):
            return product
    return "Product not found!"

@app.post("/product")
def add_product(product: Products):
    products.append(product)
    return "Product added successfully!"

@app.put("/product")
def update_product(id: int, product: Products):
    for p in products:
        if (p.id == id):
            p.id = product.id
            p.name = product.name
            p.description = product.description
            p.price = product.price
            p.quantity = product.quantity
            return ("Product updated Successfully!")
    return ("Product not found with the given ID!")

@app.delete("/product")
def delete_product(id: int):
    for i in range(len(products)):
        if(products[i].id == id):
            del products[i]
            return "Product deleted Successfully!"
    return "Product not found with the give ID!"