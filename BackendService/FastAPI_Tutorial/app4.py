from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel


app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None

# Recap
# FastAPI looks at
# -- path: checks if signature matches any path params
# -- query: assumes any singular signature param is a query param
# -- body: checks if signature is type-annotated with a Pydantic model
2

# Multiple body parameters
# -- Request body is expected to be a JSON with multiple keys
# -- "item" -> Parameters of Item model
# -- "user" -> Parameters of User model
# -- "importance" -> Since it is annotated with Body, FastAPI expects it at body instead of treating as query parameter
@app.put("/items/{item_id}")
async def update_item(
    item_id: int, item: Item, user: User, importance: Annotated[int, Body()]
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results