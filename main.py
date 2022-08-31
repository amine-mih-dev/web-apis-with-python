from bin.filters import apply_filter, apply_custom_filter
from typing import List , Optional, Union
from enum import Enum
from pydantic import BaseModel
from fastapi import FastAPI , File , UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse
import io


# Read the PIL document to find out which filters are available out-of the box
filters_available = ["blur" ,
                    "contour" ,
                    "detail" ,
                    "edge_enhance" ,
                    "edge_enhance_more" ,
                    "emboss" ,
                    "find_edges" ,
                    "sharpen" ,
                    "smooth" ,
                    "smooth_more"
                    ]
custom_filters = ["sepia", "black_and_white", "invert"]

fake_items_db = [{"item_name": "Foo"} , {"item_name": "Bar"} , {"item_name": "Baz"}]

class Filters(str, Enum):
    BLUR = "blur"
    CONTOUR = "contour"
    DETAIL = "detail"
    EDGE_ENHANCE = "edge_enhance"
    EDGE_ENHANCE_MORE = "edge_enhance_more"
    EMBOSS = "emboss"
    FIND_EDGES = "find_edges"
    SHARPEN = "sharpen"
    SMOOTH = "smooth"
    SMOOTH_MORE = "smooth_more"

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


app = FastAPI()


@app.api_route("/", methods=["GET", "POST"])
async def index():
    """
    TODO:
    1. Return the usage instructions that specifies which filters are available, and the method format
    """
    response = {"filters_available": filters_available+custom_filters,
                "usage": {"method": "POST", "url": "/<filter_available>"}
                }
    return jsonable_encoder(response)

@app.get('/items/')
async def read_items(item: Item):
    return item
@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return jsonable_encoder(item)

@app.get('/users/{user_id}/items/{item_id}')
async def read_user_item(user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

@app.post("/{filter}")
def image_filter(filter: str, img : UploadFile):
    
    """
    TODO:
    1. Checks if the provided filter is available, if not, return an error
    2. Check if a file has been provided in the POST request, if not return an error
    3. Apply the filter using apply_filter() method from bin.filters
    4. Return the filtered image as response
    """
    if (filter not in filters_available) and (filter not in custom_filters):
        return jsonable_encoder({"error": "Incorrect filter"})

    if not img: 
        return jsonable_encoder({"error": "No image provided"})
    #img = img.filename
    if filter in filters_available:
        filtered_image = apply_filter(img.file, filter)
    elif filter in custom_filters:
        filtered_image = apply_custom_filter(img.file, filter)
    return StreamingResponse( filtered_image , media_type = "image/jpeg" )

@app.get("/enum/{filter}")
async def get_filter(filter: Filters):
    return {"does filter exist?": filter in Filters}

if __name__ == "__main__":
    app.run()
    