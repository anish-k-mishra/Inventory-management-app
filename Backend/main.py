from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from models import Products
from database import session, engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

# CORS issue to connect to front-end
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"]
)

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

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()
    count = db.query(database_models.Products).count

    if count==0:

        for product in products:
            db.add(database_models.Products(**product.model_dump())) # ** for unpacking of dict to key-value pair, model_dump() gives the dictionary from the object
        db.commit()

init_db()

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)): #Dependency Injection
    # db connection 
    db_products = db.query(database_models.Products).all() #get all products from db
    
    return db_products

@app.get("/product/{id}")
def get_product_by_id(id: int , db: Session = Depends(get_db)):
    db_product = db.query(database_models.Products).filter(database_models.Products.id == id).first()
    
    if(db_product):
        return db_product
    return "Product not found!"

@app.post("/product")
def add_product(product: Products, db: Session = Depends(get_db)):
    db.add(database_models.Products(**product.model_dump()))
    db.commit()
    return "Product added successfully!"

@app.put("/product")
def update_product(id: int, product: Products, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Products).filter(database_models.Products.id == id).first()
    if (db_product):
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return ("Product updated Successfully!")
    return ("Product not found with the given ID!")

@app.delete("/product")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Products).filter(database_models.Products.id == id).first()
    
    if(db_product ):
        db.delete(db_product)
        db.commit()
        return "Product deleted Successfully!"
    return "Product not found with the give ID!"