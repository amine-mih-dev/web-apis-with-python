from typing import Optional, List
from fastapi import FastAPI, Query
from fastapi.encoders import jsonable_encoder
from model.dbHandler import match_exact, match_like


app = FastAPI()


@app.get("/")
def index():
    """
    DEFAULT ROUTE
    This method will
    1. Provide usage instructions formatted as JSON
    """
    response = {"usage": "/ddict!=<word>"}
    return jsonable_encoder(response)


@app.get("/dict")
def dictionary( words: List[str] = Query(None) ):
    """
    DEFAULT ROUTE
    This method will
    1. Accept a word from the request
    2. Try to find an exact match, and return it if found
    3. If not found, find all approximate matches and return
    """
    if not words:
        response ={"status":"error","word":words,"error": "No word provided"}
        return jsonable_encoder(response)
    responses = {"words":[]}

    for word in words:
        word = word.capitalize()
        definition = match_exact(word)
        if definition:
            response = {"status":"success","word":word,"definition":definition}
            responses["words"].append(response)
        else:
            definition = match_like(word)
            if definition:
                response = {"status":"partial","word":word,"definition":definition}
                responses["words"].append(response)
            else:
                response = {"status":"error","word":word,"error": "No definition found"}
                responses["words"].append(response)
    return responses
