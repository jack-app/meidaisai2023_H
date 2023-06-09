# モジュールをインポート
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import MeCab
from aiofiles import open

# FastAPIを起動
app = FastAPI()

# ミドルウェア(ここはあんまり考えなくてもいい)
app.add_middleware(
    CORSMiddleware, # アクセスにCORSを使用
    allow_origins=["*"], # クロスオリジンの許可するリスト
    allow_credentials=True, # クッキーの共有を許可するか
    allow_methods=["*"], # 許可するHTTPメソッド
    allow_headers=["*"], # 許可するヘッダー
)

tagger = MeCab.Tagger() # MeCabのインスタンス

@app.get("/") # ホームディレクトリ

# ボタン投下後の処理を並行処理で受け取る
async def root(text = None):
    result = tagger.parseToNode(text) # 形態素分析の結果を返す
    node = result
    response = [] # レスポンスをリストで格納

    while node: # 分析結果が残っているか

        # node.surfaceは形態素分析された単語
        # node.featureは形態素分析の結果
        print(node.surface)
        print(node.feature.split(",")) 

        if node.surface: # node.surfaceが存在する場合
            response.append(node.surface) # 形態素分析された単語をレスポンスに追加
        node = node.next # 次の形態素分析結果に移る

    return {"list":response} # レスポンスを返す

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