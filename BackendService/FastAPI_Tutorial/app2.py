from typing import Annotated

import uvicorn
from fastapi import FastAPI, Query, Path

app = FastAPI()


# Here we are using Query() because this is a query parameter.
# Later we will see others like Path(), Body(), Header(), and Cookie(),
# that also accept the same arguments as Query().
@app.get("/items/")
async def read_items(
    # Annotated -> Type annotations with metadata
    # FastAPI uses the metadata to perform further validations
    # Note that we can also pass a default value as usual
    # -- In this example, we also define a regex expression which should be matched
    q: Annotated[
        str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$")
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


if __name__ == "__main__":
    uvicorn.run(app)