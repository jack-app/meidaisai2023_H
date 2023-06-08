from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import MeCab
from aiofiles import open

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

#MeCabの形態素解析をラップ
@app.get("/")
def root(text = None):
    result = tagger.parseToNode(text)
    node = result
    response = []
    while node:
        print(node.surface,node.feature.split(","))
        if node.surface:
            response.append(node.surface)
        node = node.next
    return {"list":response}

#渡されたtextをwords.datに追記
@app.get("/write")
async def write(string):
    async with open("./src/words.dat","a",encoding="utf-8") as f:
        await f.write("\n"+string)
    return {}

#words.datに保存された内容を読み出し
@app.get("/read")
async def read():
    async with open("./src/words.dat","r",encoding="utf-8") as f:
        content = await f.read()
    return {"list":content.split("\n")}