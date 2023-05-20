from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import MeCab

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "null"
    ],
    allow_credentials=True,
    allow_methods=["*"]
)

tagger = MeCab.Tagger()

@app.get("/")
async def root(text = None):
    result = tagger.parseToNode(text)
    node = result
    response = []
    while node:
        print(node.surface,node.feature.split(","))
        if node.surface:
            response.append(node.surface)
        node = node.next
    return {"list":response}