from fastapi import FastAPI,Depends
from models import Product
from database import session,engine
import database_models
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



database_models.Base.metadata.create_all(bind = engine) 

products = [
    Product(id=1, name="phone", price=450, quantity=10, description="budget phone"),
    Product(id=2, name="laptop", price=5000, quantity=3, description="budget laptop"),
    Product(id=3, name="charger", price=1000, quantity=2, description="Mobile charger"),
    Product(id=4, name="laptop stand", price=100, quantity=1, description="laptop stand"),
]

def init_db():
    db = session()
    count = db.query(database_models.Product).count()
    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))

        db.commit()

init_db()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def greet():
    return "Hello world"

@app.get("/products")
def get_products(db:Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all() 
    # db = session
    return db_products


@app.get("/products/{id}")
def get_products_by_id(id: int,db: Session = Depends(get_db)):
    db_product =db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code= 404, detail="Product not found")
    
    return db_product
    # if db_product:
    #     return db_product

    # return {"message": "Product not found"}

@app.post("/products")
def add_product(product: Product,db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product
    



@app.put("/products/{id}")
def update(id :int, product: Product,db: Session = Depends(get_db)):
    db_product =db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.quantity = product.quantity
        db_product.price = product.price
        db.commit()
        return "update data succesfully"
    else:
     return "no product found"

@app.delete("/products/{id}")
def delete_product(id : int,db: Session = Depends(get_db)):
    db_product =db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product has been deleted"
    else:
     return "Product does not found"