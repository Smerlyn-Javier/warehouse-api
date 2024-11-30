from fastapi import FastAPI, HTTPException
from database import get_products_collection
from models import Product
from bson import ObjectId
from bson.errors import InvalidId


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8100"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

products_collection = get_products_collection()


def product_serializer(product):
    product["_id"] = str(product["_id"])
    return product

@app.get("/")
def read_root():
    return {"message": "Warehouse API is running"}


@app.get("/products/")
def get_products():
    products = list(products_collection.find())
    return {"products": [product_serializer(product) for product in products]}


@app.get("/products/{product_id}")
def get_product(product_id: str):
    try:
        product = products_collection.find_one({"_id": ObjectId(product_id)})
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product_serializer(product)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid product ID")


@app.post("/products/")
def create_product(product: Product):
    result = products_collection.insert_one(product.dict())
    return {"id": str(result.inserted_id)}

@app.put("/products/{product_id}")
def update_product(product_id: str, product: Product):
    try:
        result = products_collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": product.dict()}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"message": "Product updated"}
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid product ID")

@app.delete("/products/{product_id}")
def delete_product(product_id: str):
    try:
        result = products_collection.delete_one({"_id": ObjectId(product_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"message": "Product deleted"}
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid product ID")
    