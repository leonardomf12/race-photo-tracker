from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

# Docs
# -- If we adhere to type annotations, Enums, Pydantic models, ..., FastAPI auto-gens docs for us

# Request body: Client -> API
# Response body: API -> Client
# -- e.g.: POST methods
# -- Use Pydantic to declare response bodies


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None



app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Path parameters
# -- Name in resource path should match name in the function signature
# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": item_id}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}



# FastAPI support paths as parameters
# (But OpenAPI standard does not!)
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


# Query parameters
# -- Additional parameters not named in resource path
# -- e.g.: http://127.0.0.1:8000/items/?skip=0&limit=10

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

# Optional query parameters
# -- Annotate type as option (and in this example, default to None)
# -- Query types are also converted
# -- e.g.: http://127.0.0.1:8000/items/foo?short=1
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# Multiple path and query parameters
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item



@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

# Here, we mix request body + path + query parameters
# The function parameters will be recognized as follows:
# -- If the parameter is also declared in the path, it will be used as a path parameter.
# -- If the parameter is of a singular type (like int, float, str, bool, etc.) it will be interpreted as a query parameter.
# -- If the parameter is declared to be of the type of Pydantic model, it will be interpreted as a request body.
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result